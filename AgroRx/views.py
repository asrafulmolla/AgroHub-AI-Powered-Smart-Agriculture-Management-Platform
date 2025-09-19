import os
import base64
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .forms import IssueForm
from .models import Issue


# ---------- Helper: AI analysis ----------
import os
import base64
import requests
import time
from django.conf import settings

def analyze_image_with_openai(image_path, max_retries=3, backoff_factor=5):
    """
    Analyze an image using OpenAI GPT-4.1-mini model with retry on 429 errors.
    """
    OPENAI_API_KEY = getattr(settings, "OPENAI_API_KEY", None)
    if not OPENAI_API_KEY:
        return "⚠️ AI key not configured. Please set OPENAI_API_KEY in settings."

    # Read image and convert to base64
    try:
        with open(image_path, "rb") as f:
            img_bytes = f.read()
        b64 = base64.b64encode(img_bytes).decode("utf-8")
    except Exception as e:
        return f"❌ Failed to read image: {e}"

    endpoint = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    prompt = (
        "তুমি একজন কৃষি বিশেষজ্ঞ। ছবিটি দেখে রোগ বা সমস্যার ধরন নির্ধারণ করো "
        "এবং বাংলায় সংক্ষিপ্তভাবে চিকিৎসা/প্রেসক্রিপশন দাও।"
    )

    payload = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": f"data:image/png;base64,{b64}"}
                ]
            }
        ],
        "max_output_tokens": 500,
    }

    # Retry logic for 429 errors
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            # Parse AI response
            text = ""
            if "output" in data:
                for block in data["output"]:
                    if block.get("role") == "assistant":
                        for c in block.get("content", []):
                            if c.get("type") == "output_text":
                                text += c.get("text", "")
            return text.strip() if text else "⚠️ AI কোন পরামর্শ দিতে পারেনি।"

        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429:
                wait_time = backoff_factor * attempt
                print(f"⚠️ Rate limit hit, retrying in {wait_time} seconds... (Attempt {attempt}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
                return f"❌ AI HTTP error: {e}"
        except Exception as e:
            return f"❌ AI analysis failed: {e}"

    return "⚠️ Too many requests. অনুগ্রহ করে কিছুক্ষণ পরে চেষ্টা করুন।"


# ---------- Main View ----------
def report_issue(request):
    """
    Page where farmer uploads a single image + title/description.
    After save, AI suggestion is generated and stored.
    """
    if request.method == "POST":
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)

            # farmer attach (if login system exists)
            if request.user.is_authenticated:
                issue.farmer = request.user
            else:
                issue.farmer = None  # or handle anonymous

            issue.save()

            # AI suggestion
            image_path = issue.image.path
            ai_text = analyze_image_with_openai(image_path)
            issue.ai_suggestion = ai_text
            issue.status = "ai_suggested"
            issue.save()

            messages.success(request, "✅ ইমেজ আপলোড হয়েছে এবং AI বিশ্লেষণ সম্পন্ন হয়েছে।")
            return redirect("AgroRx:my_issue_detail", pk=issue.pk)
        else:
            messages.error(request, "⚠️ ফর্মে ভুল আছে, অনুগ্রহ করে ঠিক করুন।")
    else:
        form = IssueForm()

    return render(request, "diagnosis/report_issue.html", {"form": form})




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Issue
from .forms import ExpertPrescriptionForm

# Check if user is Krishibid
def is_krishibid(user):
    return user.groups.filter(name='Krishibid').exists()

@login_required
@user_passes_test(is_krishibid)
def issue_list(request):
    issues = Issue.objects.all()
    return render(request, 'issues/issue_list.html', {'issues': issues})

@login_required

def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    
    if request.method == 'POST':
        form = ExpertPrescriptionForm(request.POST, instance=issue)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = "solved"  # automatically update status
            obj.save()
            return redirect('AgroRx:issue_list')
    else:
        form = ExpertPrescriptionForm(instance=issue)

    return render(request, 'issues/issue_detail.html', {'issue': issue, 'form': form})


@login_required
def issue_pdf_view(request, pk):
    """
    Show a PDF-like report page for an issue.
    User can click Print button to open browser print dialog.
    """
    issue = get_object_or_404(Issue, pk=pk, farmer=request.user)
    return render(request, 'issues/issue_pdf_view.html', {'issue': issue})
 
 
 



##user admin view to see all issues
@login_required
def my_issues(request):
    """
    Show list of issues only for current farmer (logged-in user)
    """
    issues = Issue.objects.filter(farmer=request.user).order_by('-created_at')
    return render(request, 'issues/my_issues.html', {'issues': issues})

@login_required
def my_issue_detail(request, pk):
    """
    Show detail of a single issue (farmer-only)
    """
    issue = get_object_or_404(Issue, pk=pk, farmer=request.user)
    return render(request, 'issues/my_issue_detail.html', {'issue': issue})

 
 
 
 
 
 
 
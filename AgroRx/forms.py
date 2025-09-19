from django import forms
from .models import Issue

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Short title / problem statement"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class ExpertPrescriptionForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['expert_prescription']

 
 
 
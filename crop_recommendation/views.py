from django.shortcuts import render
import numpy as np
import pickle
from datetime import datetime
from .models import CropPrediction 
from .forms import CropPredictionForm
from django.contrib.auth.decorators import login_required



# Load pre-trained model and scalers
model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
mx = pickle.load(open('minmaxscaler.pkl', 'rb'))

# Crop information dictionary
    
    
crop_info = {
    1: {"name": "চাল", "icon": "🍚", "description": "চাল পৃথিবীর অনেক মানুষের প্রধান খাদ্যশস্য।"},
    2: {"name": "ভুট্টা", "icon": "🌽", "description": "ভুট্টা খাদ্য, প্রাণী খাওয়ানো এবং বায়োফুয়েল উৎপাদনের জন্য ব্যাপকভাবে চাষ করা হয়।"},
    3: {"name": "তুলা", "icon": "🧵", "description": "তুলা শক্ত ফাইবারের জন্য পরিচিত যা ব্যাগ এবং হেসিয়ান কাপড় তৈরিতে ব্যবহৃত হয়।"},
    4: {"name": "পাট", "icon": "👕", "description": "পাট একটি নরম ফাইবার যা টেক্সটাইল এবং পোশাক তৈরির জন্য ব্যবহৃত হয়।"},
    5: {"name": "নারকেল", "icon": "🥥", "description": "নারকেল বহুমুখী এবং খাদ্য, পানীয় ও তেল উৎপাদনে ব্যবহৃত হয়।"},
    6: {"name": "পেঁপে", "icon": "🍈", "description": "পেঁপে একটি উষ্ণমন্ডলীয় ফল যা মিষ্টি স্বাদ এবং স্বাস্থ্য উপকারিতার জন্য পরিচিত।"},
    7: {"name": "কমলা", "icon": "🍊", "description": "কমলা সাইট্রাস জাতীয় ফল যা ভিটামিন সি সমৃদ্ধ।"},
    8: {"name": "আপেল", "icon": "🍎", "description": "আপেল একটি জনপ্রিয় ফল যা তার খসখসে টেক্সচার এবং বিভিন্ন স্বাদের জন্য পরিচিত।"},
    9: {"name": "মিষ্টি তরমুজ", "icon": "🍈", "description": "মিষ্টি তরমুজ একটি মিষ্টি, রসালো ফল যা গরমের সময় বেশ জনপ্রিয়।"},
    10: {"name": "তরমুজ", "icon": "🍉", "description": "তরমুজ একটি সতেজকারী ফল যা পানির পরিমাণে বেশ সমৃদ্ধ।"},
    11: {"name": "আঙ্গুর", "icon": "🍇", "description": "আঙ্গুর ছোট, রসালো ফল যা খাওয়ার জন্য এবং মদ তৈরির জন্য ব্যবহৃত হয়।"},
    12: {"name": "আম", "icon": "🥭", "description": "আম একটি উষ্ণমন্ডলীয় ফল যা 'ফলরাজ' নামে পরিচিত, তার মিষ্টি স্বাদের জন্য।"},
    13: {"name": "কলা", "icon": "🍌", "description": "কলা একটি জনপ্রিয় স্ন্যাক ফল যা পটাসিয়ামে সমৃদ্ধ।"},
    14: {"name": "ডালিম", "icon": "🍎", "description": "ডালিম তার রসালো এবং অ্যান্টিঅক্সিডেন্টে সমৃদ্ধ বীজের জন্য পরিচিত।"},
    15: {"name": "মসুর ডাল", "icon": "🍲", "description": "মসুর ডাল একটি প্রোটিন সমৃদ্ধ ডাল যা বিভিন্ন খাবার এবং স্যুপে ব্যবহৃত হয়।"},
    16: {"name": "মাসকলাই ডাল", "icon": "🫘", "description": "মাসকলাই ডাল একটি ডাল যা দক্ষিণ এশীয় রান্নায় ব্যাপকভাবে ব্যবহৃত হয়।"},
    17: {"name": "মুগ ডাল", "icon": "🌱", "description": "মুগ ডাল ছোট সবুজ ডাল যা স্যুপ ও সালাদে ব্যবহৃত হয় এবং অঙ্কুরিত অবস্থায়ও খাওয়া হয়।"},
    18: {"name": "মোথ ডাল", "icon": "🫘", "description": "মোথ ডাল একটি খরা সহিষ্ণু ডাল যা ভারতীয় রান্নায় ব্যবহৃত হয়।"},
    19: {"name": "পিপড়ে ডাল", "icon": "🌿", "description": "পিপড়ে ডাল একটি সাধারণ ডাল যা প্রোটিন সমৃদ্ধ এবং গরমের আবহাওয়ায় ভালো জন্মে।"},
    20: {"name": "কিডনি ডাল", "icon": "🫘", "description": "কিডনি ডাল একটি জনপ্রিয় ডাল যা চিলি এবং সিদ্ধ করা খাবার তৈরিতে ব্যবহার করা হয়।"},
    21: {"name": "চানা ডাল", "icon": "🥙", "description": "চানা ডাল একটি বহুমুখী ডাল যা হুমাস ও তরকারির মতো বিভিন্ন খাবারে ব্যবহৃত হয়।"},
    22: {"name": "কফি", "icon": "☕", "description": "কফি একটি গুরুত্বপূর্ণ বাণিজ্যিক ফসল, যা একটি জনপ্রিয় পানীয় হিসেবে বিশ্বব্যাপী পরিচিত।"}
}

def index(request):
    current_time_date = datetime.now()
    products = CropPrediction.objects.all()
    count = products.count()
    products = CropPrediction.objects.all().order_by('-timestamp')[:30]
    context = {
        'current_time_date': current_time_date,
        'products': products,
        'count': count,
    }
    print(count)
    return render(request, "index.html", context)

def about(request):

    return render(request, "about.html") 

def iot(request):

    return render(request, "iot.html")  

@login_required
def predict(request):
    current_time_date = datetime.now()
    form = CropPredictionForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        # Extract data from form
        N = form.cleaned_data['nitrogen']
        P = form.cleaned_data['phosphorus']
        K = form.cleaned_data['potassium']
        temp = form.cleaned_data['temperature']
        humidity = form.cleaned_data['humidity']
        ph = form.cleaned_data['ph']
        rainfall = form.cleaned_data['rainfall']
        
        # Prepare and scale features for prediction
        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)
        
        # Apply MinMaxScaler and StandardScaler
        mx_features = mx.transform(single_pred)
        sc_mx_features = sc.transform(mx_features)
        
        # Predict crop
        prediction = model.predict(sc_mx_features)
        crop = crop_info.get(prediction[0], {"name": "Unknown crop", "icon": "❓", "description": "No description available."})
        
        # Save prediction to database
        CropPrediction.objects.create(
            nitrogen=N, 
            phosphorus=P, 
            potassium=K, 
            temperature=temp, 
            humidity=humidity, 
            ph=ph, 
            rainfall=rainfall, 
            predicted_crop=crop['name']
        )
        
        # Render the result
        return render(request, 'predict.html', {
            'result': crop['name'],
            'icon': crop['icon'],
            'description': crop['description'],
            'current_time_date': current_time_date
        })
    
    return render(request, 'predict.html', {'form': form, 'current_time_date': current_time_date})

    
    
    
   
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    user = request.user
    
    if user.groups.filter(name='Farmer').exists():
        # Farmer dashboard
        return redirect('AgroRx:my_issues')
    
    elif user.groups.filter(name='Krishibid').exists():
        # Krishibid dashboard
        return redirect('AgroRx:issue_list')
    
    else:
        # Default dashboard / or error page
        return render(request, 'profile.html', {'message': 'No dashboard assigned for your role.'})

   
    
    
    
#     crop_info = {
#     1: {"name": "Rice", "icon": "🍚", "description": "Rice is a staple food crop for a large part of the world's population."},
#     2: {"name": "Maize", "icon": "🌽", "description": "Maize is widely grown for food, animal feed, and biofuel production."},
#     3: {"name": "Jute", "icon": "🧵", "description": "Jute is known for its strong fibers used in making burlap and hessian cloth."},
#     4: {"name": "Cotton", "icon": "👕", "description": "Cotton is a soft fiber used in the production of textiles and clothing."},
#     5: {"name": "Coconut", "icon": "🥥", "description": "Coconuts are versatile and used in food, drink, and oil production."},
#     6: {"name": "Papaya", "icon": "🍈", "description": "Papaya is a tropical fruit known for its sweet taste and health benefits."},
#     7: {"name": "Orange", "icon": "🍊", "description": "Oranges are citrus fruits popular for their vitamin C content."},
#     8: {"name": "Apple", "icon": "🍎", "description": "Apples are a popular fruit known for their crisp texture and variety of flavors."},
#     9: {"name": "Muskmelon", "icon": "🍈", "description": "Muskmelon is a sweet, juicy fruit often enjoyed in summer."},
#     10: {"name": "Watermelon", "icon": "🍉", "description": "Watermelon is a refreshing fruit high in water content."},
#     11: {"name": "Grapes", "icon": "🍇", "description": "Grapes are small, juicy fruits used for snacking and making wine."},
#     12: {"name": "Mango", "icon": "🥭", "description": "Mango is a tropical fruit known as the 'king of fruits' for its sweet flavor."},
#     13: {"name": "Banana", "icon": "🍌", "description": "Bananas are a convenient snack fruit rich in potassium."},
#     14: {"name": "Pomegranate", "icon": "🍎", "description": "Pomegranates are known for their juicy, antioxidant-rich seeds."},
#     15: {"name": "Lentil", "icon": "🍲", "description": "Lentils are a protein-rich legume used in various dishes and soups."},
#     16: {"name": "Blackgram", "icon": "🫘", "description": "Blackgram is a legume commonly used in South Asian cuisine."},
#     17: {"name": "Mungbean", "icon": "🌱", "description": "Mungbeans are small green beans often used in soups and sprouted salads."},
#     18: {"name": "Mothbeans", "icon": "🫘", "description": "Mothbeans are drought-resistant legumes used in Indian dishes."},
#     19: {"name": "Pigeonpeas", "icon": "🌿", "description": "Pigeonpeas are a common legume grown for their protein content."},
#     20: {"name": "Kidneybeans", "icon": "🫘", "description": "Kidneybeans are a popular legume used in chili and stews."},
#     21: {"name": "Chickpea", "icon": "🥙", "description": "Chickpeas are versatile legumes used in dishes like hummus and curry."},
#     22: {"name": "Coffee", "icon": "☕", "description": "Coffee is an important cash crop, known for producing a popular beverage."}
# }

from django.shortcuts import render
from .models import Crop
import requests

def irrigation_schedule(request):
    crops = Crop.objects.all()
    selected_crop = None
    decision = None

    if request.method == "POST":
        # ✅ Crop selection
        crop_id = request.POST.get("crop_id")
        selected_crop = Crop.objects.get(id=crop_id)

        # ✅ User location (fallback to Dhaka)
        LAT = request.POST.get("lat")
        LON = request.POST.get("lon")
        try:
            LAT = float(LAT) if LAT else 23.8103
            LON = float(LON) if LON else 90.4125
        except ValueError:
            LAT, LON = 23.8103, 90.4125

        API_KEY = "2c8079b2c3e601e75fe64d5d095748e6"  # OpenWeatherMap API Key

        # 🔹 Weather API call
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {"lat": LAT, "lon": LON, "appid": API_KEY, "units": "metric"}
        try:
            res = requests.get(url, params=params, timeout=10).json()
        except requests.RequestException:
            res = {}
            decision = "⚠️ Weather data fetch failed. Default irrigation will be used."
            water_amount = selected_crop.base_water_litre
        else:
            # ✅ Next 24h Rainfall (8×3h forecast)
            rain_forecast = 0
            if "list" in res and len(res["list"]) > 0:
                for entry in res["list"][:8]:
                    rain_forecast += entry.get("rain", {}).get("3h", 0)

            # 🔹 Irrigation Decision Logic
            if rain_forecast >= 20:
                water_amount = 0
                decision = f"⛔ {selected_crop.name} এর জন্য সেচ বাতিল (expected rain {rain_forecast:.1f}mm)"
            elif rain_forecast >= 10:
                water_amount = selected_crop.base_water_litre * 0.75
                decision = f"💧 {selected_crop.name} এর জন্য 25% কমানো হয়েছে → {water_amount:.1f} লিটার/m²"
            elif rain_forecast >= 5:
                water_amount = selected_crop.base_water_litre * 0.50
                decision = f"💧 {selected_crop.name} এর জন্য 50% কমানো হয়েছে → {water_amount:.1f} লিটার/m²"
            else:
                water_amount = selected_crop.base_water_litre
                decision = f"💦 {selected_crop.name} এর জন্য ফুল সেচ → {water_amount:.1f} লিটার/m²"

    return render(request, "crops/irrigation.html", {
        "crops": crops,
        "selected_crop": selected_crop,
        "decision": decision,
    })

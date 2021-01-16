from django.shortcuts import render, redirect
from decouple import config
import requests
from pprint import pprint
from .models import City
from .forms import CityForm
from django.contrib import messages

def index(request):
    form = CityForm()
    cities = City.objects.all()
    url = config("BASE_URL")

    if request.method == "POST":
        form = CityForm(request.POST) #request.POST.get("name")
        if form.is_valid():
            new_city = form.cleaned_data["name"]
            if not City.objects.filter(name=new_city).exists():
                r = requests.get(url.format(new_city))
                if r.status_code == 200:
                    form.save()
                    messages.success(request, "City added succesfully!")
                else:
                    messages.warning(request, "City does not exist.")
            else:
                messages.warning(request, "City already exists.")
            return redirect("home")


    city_data = []
    for city in cities:
        #print(city)
        r = requests.get(url.format(city))
        content= r.json()  

        weather_data = {
        'city' : city.name,
        'temp' : content['main']['temp'],
        'description': content['weather'][0]["description"],
        "icon" : content["weather"][0]["icon"]
         }
        city_data.append(weather_data)

    context = {
       "city_data": city_data,
       "form" : form
    }
    return render(request, "weather/index.html", context)

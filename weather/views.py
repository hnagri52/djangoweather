from django.shortcuts import render
import requests
import json
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):


    apikey = '9966b3a3616366d6a2550a03fbc11dd3'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=9966b3a3616366d6a2550a03fbc11dd3'

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()
        print(request.POST)

    form = CityForm() #this is not in the if statement cuz once u submit the form, u want the form to be blank again





    cities = City.objects.all()

    weather_data = []

    for city in cities:



        response = requests.get(url.format(city)).json()

       # print(response)
        city_weather = {
            "city" : city.name,
            "temperature": "{:.2f}".format(float(response["main"]["temp"])-273.15),
            "description":response["weather"][0]["description"],
            "icon": response["weather"][0]["icon"],

        }

        weather_data.append(city_weather)

      #  print(city_weather)
      #  print(weather_data)


    context = {"weather_data": weather_data, "form" : form}
   # print(context)

    return render(request,"weather/weather.html", context)

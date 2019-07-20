from django.shortcuts import render,redirect
import requests
import json
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):


    apikey = '9966b3a3616366d6a2550a03fbc11dd3'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=9966b3a3616366d6a2550a03fbc11dd3'


    message = ""
    message_class = ""

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data["name"]
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                re = requests.get(url.format(new_city)).json()
                if re["cod"] == 200:
                 form.save()
                else:
                    error_msg = "City does not exist in the world"
            else:
                error_msg = 'The city already exists in the table!'

        if error_msg:
            message = error_msg
            message_class = "is-danger"
        else:
            message = "City succesfully added"
            message_class = "is-success"

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


    context = {
        "weather_data": weather_data,
        "form" : form,
        "message" : message,
        "message_class" : message_class
    }
   # print(context)

    return render(request,"weather/weather.html", context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home"')
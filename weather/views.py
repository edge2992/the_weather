import requests
from django.shortcuts import render

# Create your views here.
from weather.env import API_Key
from weather.forms import CityForm
from weather.models import City


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid='+API_Key


    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    #city = 'Las Vegas'
    cities = City.objects.all()
    form = CityForm()
    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()

        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
        }

        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context)
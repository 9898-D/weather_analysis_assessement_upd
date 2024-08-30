from django.shortcuts import render
from .utils import fetch_weather_data
from .models import WeatherData
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render


from .forms import CityForm

def weather_view(request, city):
    data = fetch_weather_data(city)
    if data:
        weather = WeatherData.objects.create(
            city=data['city'],
            temperature=data['temperature'],
            humidity=data['humidity'],
            condition=data['condition'],
            wind_speed=data['wind_speed'],
            pressure=data['pressure'],
            visibility=data['visibility'],
            uv_index=data['uv_index'],
            feels_like=data['feels_like']
        )
        weather.save()

        weather_data = WeatherData.objects.filter(city=city).order_by('-recorded_at')[:24]
        avg_temp = sum([w.temperature for w in weather_data]) / len(weather_data)
        context = {
            'weather': weather,
            'avg_temp': avg_temp,
            'is_extreme': weather.temperature > 35 or weather.temperature < 0,
        }
        return render(request, 'weather.html', context)
    else:
        return JsonResponse({"Message": f"Given city '{city}' doesn't exist. Please provide a valid city name."})



def home_page(request):
    # if this is a POST request we need to process the form data
    print(request.method)
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CityForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            city = form.cleaned_data["city"]
            return HttpResponseRedirect(f"weather/{city}")

    else:
        form = CityForm()

    return render(request, "home_page.html", {"form": form})
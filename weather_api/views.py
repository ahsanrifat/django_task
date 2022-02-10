from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .decorators_custom import timeit

weather_api_key = "4850342c56619e5ba0c502c2dd9ab4f1"


@api_view(["GET"])
@timeit
def weather_of_a_city(request):
    city_name = request.GET.get("city")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city_name, "appid": "4850342c56619e5ba0c502c2dd9ab4f1"}
    return_data = requests.get(url, params=params).json()
    return Response({"message": return_data})

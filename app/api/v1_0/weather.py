from flask import Blueprint, jsonify, request
import requests

weather = Blueprint("weather", __name__)


@weather.route("/weather/index")
def get_weather_index():
    longitude = request.args.get("longitude")
    latitude = request.args.get("latitude")
    # url = "https://api.caiyunapp.com/v2.5/uy75odfSWI3WbQJj/117.216447%2C36.664459/weather?alert=true&dailysteps=1"
    url = "https://api.caiyunapp.com/v2.5/uy75odfSWI3WbQJj/%s,%s/weather?alert=true&dailysteps=1" % (
        longitude, latitude)
    res = requests.get(url)
    print(res.text)
    return res.json()


@weather.route("/weather/detail")
def get_weather_detail():
    longitude = request.args.get("longitude")
    latitude = request.args.get("latitude")
    url = "https://api.caiyunapp.com/v2.5/uy75odfSWI3WbQJj/%s,%s/daily?dailysteps=15" % (
        longitude, latitude)
    res = requests.get(url)
    return res.json()

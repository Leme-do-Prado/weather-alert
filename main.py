import os

import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

#openweather api authentication
openweather_api_key = "my_key"
openweather_api_url = "https://api.openweathermap.org/data/2.5/forecast"

openweather_params = {
    "lat": "your_latitude",
    "lon": "your_longitude",
    "appid": openweather_api_key,
    "cnt": 4
}

#twilio api authentication and configs
twilio_account_sid = "my_sid"
twilio_auth_token = "my_auth_token"

response = requests.get(openweather_api_url, params=openweather_params)
response.raise_for_status()
weather_data = response.json()

is_raining = False

for weather in weather_data["list"]:
    weather_id = weather["weather"][0]["id"]
    if weather_id < 700:
        is_raining = True

if is_raining:
    twilio_proxy_client = TwilioHttpClient()
    twilio_proxy_client.session.proxies = {'https:': os.environ['https_proxy']}

    client = Client(twilio_account_sid, twilio_auth_token, http_client=twilio_proxy_client)
    message = client.messages.create(

        body="Remember to bring an umbrella — it might rain today! ☔",

        from_="+19472231734",

        to="+5513982058863",
    )
    print(message.status)

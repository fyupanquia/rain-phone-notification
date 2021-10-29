import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

#OPEN_WEATHER_MAP https://openweathermap.org/
OPEN_WEATHER_MAP_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
OPEN_WEATHER_MAP_API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")

#TWILIO https://twilio.com/
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")

#YOUR PHONE NUMBER
MY_PERSONAL_PHONE_NUMBER = os.environ.get("MY_PERSONAL_PHONE_NUMBER")

# for lat and lon : https://www.latlong.net/
weather_params = {
    "lat": "-12.046373",
    "lon": "-77.042755",
    "appid": OPEN_WEATHER_MAP_API_KEY,
    "exclude": "current,minutely,daily"
}

response = requests.get(OPEN_WEATHER_MAP_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700: # https://openweathermap.org/weather-conditions
        will_rain = True


if will_rain:
    print("Oh oh! You'd better take an umbrella")

    # Uncomment this section if you have some errors related with your proxy
    #proxy_client = TwilioHttpClient()
    #proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    #client = Client(account_sid, auth_token, http_client=proxy_client)

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_=TWILIO_PHONE_NUMBER,
        to=MY_PERSONAL_PHONE_NUMBER
    )
    print(message)
else:
    print("The weather is fine")
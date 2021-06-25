import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWN_ENDPOINT="https://api.openweathermap.org/data/2.5/onecall"
api_key=os.environ.get("OWN_API_KEYS")
account_sid = os.environ.get("OWN_API_KEY")
auth_token = os.environ.get("OWN_API_TOKEN")
# these are personal api keys if you run as it is you  moght get error
# make sure you sign in to twilio and get your own API keys(Free trail is available)
#the above variables are environmental variables (used OS) which means it wont come for  everyone.

weather_params={
    "lat":25.611219,
    "lon":85.130692,
    "appid":api_key,
    "exclude":"current,minutely,daily"
}

response=requests.get(OWN_ENDPOINT,params=weather_params)
response.raise_for_status()
weather_data=response.json()
weather_slicing=weather_data["hourly"][:12]
will_rain=False
for hour in weather_slicing:
    condition_data=hour["weather"][0]["id"]
    if int(condition_data)<700:
        will_rain=True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token,http_client=proxy_client)
    message = client.messages \
        .create(
        body="Its going to rain today. Take an Umbrella ☔",
        from_= #after signing in to twilaio you will get your own number,
        to= #give your verified number used in twilio.
    )
    print(message.status)




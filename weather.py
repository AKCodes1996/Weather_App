

import streamlit as st 
# This module used to process http request
import requests

#This module used to parse argument from cli
import argparse

# This module gives functionality towork with JSON data
import json

#This module gives functionality to work with date and time
from datetime import datetime






# This section code parse the argument passed from cli
arg_obj = argparse.ArgumentParser()

# Number of argument you want to give that many times need to add argument '''
arg_obj.add_argument("city")
arg_obj.add_argument("country")
arg = arg_obj.parse_args()




# Weather & Geo Location URL/API
geo_location_url = "https://geocoding-api.open-meteo.com/v1/search"
weacther_url = "https://api.open-meteo.com/v1/forecast"

#params for Geolocation API
params = {
    "name": arg.city,
    "count": 1,
    "language": "en",
    "format": "json"
}



#below code generate http req to geo location url and gettingn response
geolocation_res = requests.get(geo_location_url,params=params,timeout=10)
json_data = geolocation_res.json()



#Reading city lat and long from geolocation url response
lat = json_data['results'][0]["latitude"]
long = json_data['results'][0]["longitude"]



#params for weather url
weather_params = {
    "latitude": lat,
    "longitude": long,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    
}




#below code generate http req to weather url and get response
weather_res = requests.get(weacther_url,params=weather_params,timeout=10)
wea_json_res = weather_res.json()

#converting time in readbale time
dt = datetime.fromisoformat(wea_json_res['current']['time'])
readable_time = dt.strftime("%A, %d %B %Y | %I:%M:%S %p")

readable_temp = wea_json_res['current']['temperature_2m']
readable_humidity = wea_json_res['current']['relative_humidity_2m']
readable_wind_speed = wea_json_res['current']['wind_speed_10m']


  




# below code is for ui setup with streamlit
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️"
    
)


with st.container(border=True):
    st.title("🌤️ Weather Dashboard")
    st.subheader(f"Current Weather of {arg.city}")
    st.write(f"Time : {readable_time}")
    st.write(f"Temperature : {readable_temp} °C")
    st.write(f"Humidity : {readable_humidity}%")
    st.write(f"Wind Speed : {readable_wind_speed} m/s")

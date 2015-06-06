#!/usr/bin/env python
# get temperature data from external sources
# currently that means only from foreacast.io API 
# using the forecastio python library

import forecastio
import account
import ilmerree
from storage import tempdb
import time
import tempy

# Tallinn, Kesklinn
lat, lng = 59.41494, 24.74032
# my forecast.io key, kept in a separate file
key = account.forecast_io_key


while True:
    retry_count = 0
    try:
        if retry_count > 0:
            sleep_time = (retry_count * 2) + 5
            time.sleep(sleep_time)
        forecast = forecastio.load_forecast(key, lat, lng)
        break
    except:
        print "Failed to get data from forecast.io, will retry"
        retry_count += 1

current_data = forecast.currently()
forecastio_temperature = current_data.d['temperature']

ilm = ilmerree.Ilm()
ilmerree_temperature = ilm.get_temperature()
ilmerree_wind_speed = ilm.get_wind()['wind_speed']
ilmerree_wind_direction = ilm.get_wind()['wind_direction']

t = tempdb.Tempdb()
t.add_reading("forecastio_temperature", forecastio_temperature)
t.add_reading("ilmerree_temperature", ilmerree_temperature)

tempy.update({
    "source":"wipi",
    "sensor":"ilmerree_temperature", 
    "temperature":ilmerree_temperature,
    "wind_speed": ilmerree_wind_speed,
    "wind_direction": ilmerree_wind_direction
    })
tempy.update({"source":"wipi","sensor":"forecastio_temperature","temperature":forecastio_temperature})

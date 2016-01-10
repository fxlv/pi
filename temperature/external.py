#!/usr/bin/env python
# get temperature data from external sources
# currently that means only from foreacast.io API 
# using the forecastio python library

import forecastio
import account
import ilmerree
#from storage import tempdb
import time
#import tempy
import json
import sys

# Tallinn, Kesklinn
tallinn = {"lat": 59.41494, "lng": 24.74032}
# Riga, Latvia
riga = {"lat": 56.9460, "lng": 24.1149}
# my forecast.io key, kept in a separate file
key = account.forecast_io_key

jsonfile_name = "/tmp/external_temperature.json"

places = {"tallinn": tallinn, "riga": riga}
while True:
    retry_count = 0
    try:
        if retry_count > 0:
            sleep_time = (retry_count * 2) + 5
            time.sleep(sleep_time)
        for place in places:
            forecast = forecastio.load_forecast(key, places[place]["lat"], places[place]["lng"])
            current_data = forecast.currently()
            forecastio_temperature = current_data.d['temperature']
            places[place]["temperature_forecastio"] = float(forecastio_temperature)
        break
    except Exception, e:
        print "Failed to get data from forecast.io, will retry"
        print "Exception: ",e
        if retry_count == 10:
            print "Max retry cunt reached, giving up."
            sys.exit(1)
        retry_count += 1


ilm = ilmerree.Ilm()
places["tallinn"]["temperature_ilmerree"] = float(ilm.get_temperature())
ilmerree_wind_speed = ilm.get_wind()['wind_speed']
ilmerree_wind_direction = ilm.get_wind()['wind_direction']

#t = tempdb.Tempdb()
#t.add_reading("forecastio_temperature", forecastio_temperature)
#t.add_reading("ilmerree_temperature", ilmerree_temperature)

with open(jsonfile_name, "w") as jsonfile:
    jsonfile.write(json.dumps(places))


#tempy.update({
#    "source":"wipi",
#    "sensor":"ilmerree_temperature", 
#    "temperature":ilmerree_temperature,
#    "wind_speed": ilmerree_wind_speed,
#    "wind_direction": ilmerree_wind_direction
#    })
#tempy.update({"source":"wipi","sensor":"forecastio_temperature","temperature":forecastio_temperature})

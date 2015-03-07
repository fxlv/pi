#!/usr/bin/env python
# get temperature data from external sources
# currently that means only from foreacast.io API 
# using the forecastio python library

import forecastio
import account
import ilmerree
from storage import tempdb
from azurepy import queues

# Tallinn, Kesklinn
lat, lng = 59.41494, 24.74032
# my forecast.io key, kept in a separate file
key = account.forecast_io_key

forecast = forecastio.load_forecast(key, lat, lng)
current_data = forecast.currently()
forecastio_temperature = current_data.d['temperature']
forecastio_queue = queues.Queue("forecastio-temperature")

ilmerree_temperature = ilmerree.get_temperature()
ilmerree_queue = queues.Queue("ilmerree-temperature")

ttl = 300 # 5 mins
forecastio_queue.put(forecastio_temperature, ttl)
ilmerree_queue.put(ilmerree_temperature, ttl)


tempdb.add_reading("forecastio_temperature", forecastio_temperature)
tempdb.add_reading("ilmerree_temperature", ilmerree_temperature)

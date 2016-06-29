#!/usr/bin/env python
# To read DHT22 from raspberry
# clone and install: https://github.com/adafruit/Adafruit_Python_DHT.git
#
# sudo apt-get install build-essential python-dev
# sudo python setup.py install
#
#
#
import Adafruit_DHT
import json

sensor = Adafruit_DHT.DHT22
pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
print json.dumps({"humidity":humidity, "temperature":temperature})

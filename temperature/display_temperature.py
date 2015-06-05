#!/usr/bin/env python
#
# for testing and development purposes only
#
import sys
sys.path.append("../lcd")
import lcd
import datetime
import tempy


def trend(source_name):
    temperatures = {}
    temperatures_list = []
    index = 0
    for reading in t.get_all_readings(source_name, 5):
        index += 1
        temperatures[index] = reading['temperature']
        temperatures_list.append(reading['temperature'])
    if min(temperatures_list) == max(temperatures_list):
        return "Steady"
    if temperatures[1] < temperatures[5]:
        return "Rising"
    if temperatures[1] > temperatures[5]:
        return "Falling"
    return "Unknown"


def show_last_reading():
    temp_in = tempy.get_temperature("wipi-int")
    humidity_in = tempy.get_humidity("wipi-int")
    temp_out = tempy.get_temperature("ilmerree_temperature")
    msg = []
    msg.append("Temperatures")
    msg.append("Out: {0}".format(temp_out))
    msg.append("In: {0}".format(temp_in))
    msg.append("Humidity: {0}".format(humidity_in))
    lcd.write_screen(msg, 20)

if __name__ == "__main__":
    show_last_reading()

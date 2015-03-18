#!/usr/bin/env python
#
# for testing and development purposes only
#
from storage import tempdb
import sys
sys.path.append("../lcd")
import lcd
import datetime


t = tempdb.Tempdb()

def print_sources():
    print "Available sources:"
    for source in t.get_source_names():
        print " > ",source

def show_last_reading():
    for source in t.get_source_names():
        reading_count = t.get_reading_count(source)
        last_reading = t.get_last_reading(source)
        if source == "ilmerree_temperature":
            temp_out = last_reading['temperature']
        if source == "wipi-int":
            temp_in = last_reading['temperature']
        if source == "wipi-int-humidity":
            humidity_in = last_reading['temperature']
        now = datetime.datetime.now()
        reading_date = last_reading['date']
        time_delta = now - reading_date
        msg = []
        if time_delta.seconds > 400:
            msg.append("Old data for")
            msg.append("  {0}".format(last_reading['source_name']))
        else:
            msg.append("Source: ")
            msg.append("  {0}".format(last_reading['source_name']))
        msg.append("Temperature: {0}".format(last_reading['temperature']))
        msg.append("Time delta: {0}".format(time_delta.seconds))
        lcd.write_screen(msg, 5)
    msg = []
    msg.append("Temperatures")
    msg.append("Outside: {0}".format(temp_out))
    msg.append("Inside: {0}".format(temp_in))
    msg.append("Humidity: {0}".format(humidity_in))
    lcd.write_screen(msg, 20)

if __name__ == "__main__":
    print_sources()
    show_last_reading()

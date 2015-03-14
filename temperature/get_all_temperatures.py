#!/usr/bin/env python
#
# for testing and development purposes only
#
from storage import tempdb

t = tempdb.Tempdb()

def print_sources():
    print "Available sources:"
    for source in t.get_source_names():
        print " > ",source

def get_last_reading():
    print "Last readings:"
    for source in t.get_source_names():
        reading_count = t.get_reading_count(source)
        last_reading = t.get_last_reading(source)
        print " > {0} readings: {1}".format(last_reading, reading_count)

def get_all_readings():
    print "All readings:"
    for source in t.get_source_names():
        reading_count = t.get_reading_count(source)
        for reading in t.get_all_readings(source):
            print " > {0} readings: {1}".format(reading, reading_count)

if __name__ == "__main__":
    print_sources()
    get_last_reading()
    get_all_readings()

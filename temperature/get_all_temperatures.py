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
        print " > ",t.get_last_reading(source)

if __name__ == "__main__":
    print_sources()
    get_last_reading()

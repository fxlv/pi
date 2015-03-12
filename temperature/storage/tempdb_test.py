import random
import os
import sqlite3
from tempdb import Tempdb

random_number = random.randint(0,100)
test_db_name = "test_{0}.db".format(random_number)
test_source_name = "test_source_{0}".format(random_number)

t = None

def test_init():
    global t
    t = Tempdb(test_db_name)
    assert isinstance(t, Tempdb)

def test_connect():
    conn, cursor = t.connect()
    assert isinstance(conn, sqlite3.Connection)
    assert isinstance(cursor, sqlite3.Cursor)

def test_add_reading():
    test_temperature = random.randint(-10,30)
    t.add_reading(test_source_name, test_temperature)
    test_temperature = random.randint(-10,30)
    t.add_reading(test_source_name, test_temperature)

def test_get_source_names():
    source_names = t.get_source_names()
    assert len(source_names) == 1
    assert source_names[0] == test_source_name

def test_get_all_readings():
    readings = t.get_all_readings(test_source_name)
    assert len(readings) == 2
    # second column of the first row contains source name
    assert readings[0][1] == test_source_name

def test_get_last_reading():
    last_reading = t.get_last_reading(test_source_name)
    # should contain 5 columns/fields
    assert len(last_reading) == 5
    assert isinstance(last_reading, tuple)
    assert last_reading[1] == test_source_name

def test_cleanup():
    os.unlink(test_db_name)

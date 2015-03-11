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

def test_cleanup():
    os.unlink(test_db_name)

def test_add_reading():
    test_temperature = random.randint(-10,30)
    t.add_reading(test_source_name, test_temperature)
    test_temperature = random.randint(-10,30)
    t.add_reading(test_source_name, test_temperature)

def test_get_source_names():
    pass

def test_get_all_readings():
    pass

def test_get_last_reading():
    pass

import random
import os
import sqlite3
from tempdb import Tempdb

random_number = random.randint(0,100)
test_db_name = "test_{0}.db".format(random_number)
t = None

def test_init():
    global t
    t = Tempdb(test_db_name)
    assert isinstance(t, Tempdb)

def test_cleanup():
    os.unlink(test_db_name)

def test_connest():
    conn, cursor = t.connect()
    assert isinstance(conn, sqlite3.Connection)
    assert isinstance(cursor, sqlite3.Cursor)


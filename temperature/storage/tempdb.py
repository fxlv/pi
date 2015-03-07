import sqlite3
import datetime
import os

db_search_path = [
    "github/pi/temperature/temperature.db",
    "pi/temperature/temperature.db",
    "temperature.db"]


for path in db_search_path:
    if os.path.exists(path):
        db_path="{0}/{1}".format(os.getcwd(), path)
        print db_path
        break

def get_conn():
    conn = sqlite3.connect(db_path)
    return conn

def add_reading(source_name, temperature_reading):
    conn = get_conn()
    c = conn.cursor()
    now = datetime.datetime.now()
    sql = """insert into temperature values (NULL,?,?,?)"""
    sql_vars = (source_name, temperature_reading, now,)
    c.execute(sql,sql_vars)
    conn.commit()
    conn.close()

def get_reading(source_name):
    conn = get_conn()
    c = conn.cursor()
    sql = "select * from temperature where source_name=?"
    sql_vars = (source_name, now)
    c.execute(sql, sql_vars)
    return c.fetchall()



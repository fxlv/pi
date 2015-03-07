import sqlite3
import datetime

def get_conn():
    conn = sqlite3.connect("temperature.db")
    return conn

def add_reading(source_name, temperature_reading):
    conn = get_conn()
    now = datetime.datetime.now()
    sql = """insert into temperature values (NULL,'kaka','mauka','{0}')""".format(now)
    c.execute(sql)
    conn.commit()
    conn.close()

def get_reading(source_name):
    conn = get_conn()
    c = conn.cursor()
    sql = "select * from temperature where source_name=?"
    sql_vars = (source_name, now)
    c.execute(sql, sql_vars)
    return c.fetchall()



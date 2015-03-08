import sqlite3
import datetime
import os


class Tempdb:
    def __init__(self):
        self.db_search_path = [
            "github/pi/temperature/temperature.db",
            "pi/temperature/temperature.db",
            "temperature.db"]
        self.db_path = self.find_db_path()
        self.conn, self.cursor = self.connect()

    def __del__(self):
        self.conn.close()

    def find_db_path(self):
        for path in self.db_search_path:
            if os.path.exists(path):
                db_path = "{0}/{1}".format(os.getcwd(), path)
                return db_path

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        return conn, cursor

    def add_reading(self, source_name, temperature_reading):
        now = datetime.datetime.now()
        sql = """insert into temperature values (NULL,?,?,?,?)"""
        sql_vars = (source_name, temperature_reading, now, True)
        self.cursor.execute(sql, sql_vars)
        self.conn.commit()

    def get_source_names(self):
        sql = "select distinct source_name from temperature"
        self.cursor.execute(sql)
        source_names = []
        for row in self.cursor.fetchall():
            source_names.append(row[0])
        return source_names

    def get_all_readings(self, source_name):
        sql = "select * from temperature where source_name=?"
        sql_vars = (source_name,)
        self.cursor.execute(sql, sql_vars)
        return self.cursor.fetchall()
    
    def get_last_reading(self, source_name):
        sql = """select * from temperature
            where source_name=? order by insert_time desc limit 1"""
        sql_vars = (source_name,)
        self.cursor.execute(sql, sql_vars)
        return self.cursor.fetchone()

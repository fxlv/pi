"""
Get temperature from http://ilm.err.ee/
"""
from bs4 import BeautifulSoup
import requests

class Ilm:
    
    def __init__(self):
        page = requests.get("http://ilm.err.ee").text
        self.soup = BeautifulSoup(page, "lxml")

    def get_temperature(self):
        try:
            #temperature = self.soup.find("option", "ilm_tana_parem").string.strip()
            # TODO: There mus be a better way to do this, 
            # but for now this will have to do
            temperature = self.soup.findAll("option")
            # we now have all the options and need to find Tallinn amongst them
            for t in temperature:
                if "Tallinn" in str(t):
                    # if Tallinn was found, 
                    # convert to string and split by whitespaces
                    tallinn_weather = str(t).split()
                    # now search for temperature
                    # example: 'data-item-airtemperature="-18.8"'
                    for item in tallinn_weather:
                        if "airtemperature" in item:
                            # we found the temperature, now extract it as a float
                            temperature = float(item.split("=")[1].replace('"',''))
        except AttributeError:
            return False
        return temperature

    # try to translate estonian strings to english
    # (used to translate weather direction)
    def translate(self, string):
        known_strings = {
                u'l\xf5unast': 'southern', 
                u'l\xe4\xe4nest':'westerly',
                u'p\xf5hjast':'north',
                'edelast':'southwest',
                'loodest':'northwest',
        }
        if string in known_strings:
            return known_strings[string]
        else:
            return string

    def get_wind(self):
        try:
            result = self.soup.find("span", {"id": "tuul"}).string
            (wind_direction, wind_speed) = result.split()[:2]
            wind_direction = self.translate(wind_direction)
            wind_speed = float(wind_speed)
        except AttributeError, e:
            print "Got error", e
            return {"wind_direction": "error", "wind_speed": "error" }
        return {"wind_direction": wind_direction, "wind_speed":wind_speed }


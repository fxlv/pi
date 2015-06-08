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
            temperature = self.soup.find("div", "ilm_tana_parem").string.strip()
            temperature = float(temperature.split()[0])
        except AttributeError:
            return False
        return temperature

    # try to translate estonian strings to english
    # (used to translate weather direction)
    def translate(self, string):
        known_strings = {
                u'l\xf5unast': 'southern', 
                u'l\xe4\xe4nest':'westerly',
                'edelast':'southwest',
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
        except AttributeError:
            return False
        return {"wind_direction": wind_direction, "wind_speed":wind_speed }


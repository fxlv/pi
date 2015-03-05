"""
Get temperature from http://ilm.err.ee/ 
"""
from bs4 import BeautifulSoup
import requests

def get_html():
    page = requests.get("http://ilm.err.ee")
    return page.text

def get_temperature():
    soup = BeautifulSoup(get_html(), "lxml")
    temperature = soup.find("div","ilm_tana_parem").string.strip()
    # split off the celsius symbol and make it a float instead of string
    temperature = float(temperature.split()[0])
    return temperature

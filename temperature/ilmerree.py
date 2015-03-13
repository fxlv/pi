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
    try:
        temperature = soup.find("div", "ilm_tana_parem").string.strip()
        temperature = float(temperature.split()[0])
    except AttributeError:
        return False
    return temperature

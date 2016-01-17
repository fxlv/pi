#!/usr/bin/env python
#
# Get temperature value from
# Dallas DS18B20 or from DHT22
# and write the values to an 'info' file
# which can later be consumed by monitoring tools
#
import glob
import sys
import os
import tempy
import subprocess
import json
import time
from azurepy import queues
from storage import tempdb
infofile_name = "/tmp/temperature.info"
jsonfile_name = "/tmp/temperature.json"
home = os.environ['HOME']

DEBUG = True
OUTPUT_JSON = True
OUTPUT_INFOFILE = True

# sensors sometimes can return very high values
# define maximum values here
MAX_TEMP = 100 
MAX_HUMIDITY = 100 

def debugprint(msg):
    global DEBUG
    if DEBUG:
        print "DEBUG: {0}".format(msg)


def find_adafruit_dht():
    search_path = [home, '.', '/opt']
    for path in search_path:
        path = "{0}/Adafruit_DHT".format(path)
        if DEBUG:
            debugprint("Checking for {0}".format(path))
        if os.path.exists(path):
            if DEBUG:
                debugprint("Found {0}".format(path))
                return path
    else:
        return False


def write_infofile(temperature_data):
    with open(infofile_name, "w") as infofile:
        infofile.write("humidity_dht22={}\n".format(temperature_data[
            "humidity_dht22"]))
        infofile.write("temperature_dht22={}\n".format(temperature_data[
            "temperature_dht22"]))
        infofile.write("temperature_dallas={}\n".format(temperature_data[
            "temperature_dallas"]))


def write_json(temperature_data):
    with open(jsonfile_name, "w") as jsonfile:
        jsonfile.write(json.dumps(temperature_data))


def main():
    temperature_dht22 = False
    temperature_dallas = False
    humidity_dht22 = False

    # DHT needs /dev/mem access
    if os.geteuid() != 0:
        print "You need to be root in order to use DHT temperature sensor."
        print "Please run as root."
        sys.exit(1)

    onewire_list = glob.glob("/sys/bus/w1/devices/28*")
    if len(onewire_list) == 1:
        dallas_sensor_file = "{}/w1_slave".format(onewire_list[0])
        if not os.path.exists(dallas_sensor_file):
            debugprint("W1 slave file does not exist")
        with open(dallas_sensor_file) as dallas_sensor:
            lines = dallas_sensor.readlines()
            if not len(lines) == 2:
                print "Unexpected output from w1 file"
                sys.exit(1)
            try:
                temperature = lines[1].split("t=")[1]
                temperature = float(temperature) / 1000
            except:
                print "Could not parse temperature output"
                sys.exit(1)
            debugprint("Dallas sensor temperature OK")
            temperature_dallas = temperature
    else:
        debugprint("Did not find the dallas one wire sensor")

    # getting dht info can fail so we use simple retry mechanism
    dht_success = False

    # DHT can fail to return temperature or return some fynny values
    # so retry untill dht_success is True
    while not dht_success:
        adafruit_dht = find_adafruit_dht()
        if not adafruit_dht:
            print "Adafruit_DHT binary is missing"
            sys.exit(1)
        output = subprocess.check_output([adafruit_dht, "22", "4"])
        output = output.splitlines()

        if len(output) == 3:
            debugprint("OK, got information from DHT22")
            temp_and_humidity = output[2].split()
            debugprint(temp_and_humidity)
            temperature_dht22 = float(temp_and_humidity[2])
            humidity_dht22 = float(temp_and_humidity[6])
            if temperature_dht22 < MAX_TEMP and humidity_dht22 < MAX_HUMIDITY:
                dht_success = True
            else:
                # some funny values were returned by the sensors, 
                # wait and retry
                if DEBUG:
                    print "Unreasonable values returned by the sensors"
                time.sleep(1)
        else:
            debugprint("Failed to get information from DHT22")

    if DEBUG:
        debugprint(humidity_dht22)
        debugprint(temperature_dht22)

    temperature_data = {}
    temperature_data["humidity_dht22"] = float(humidity_dht22)
    temperature_data["temperature_dht22"] = float(temperature_dht22)
    temperature_data["temperature_dallas"] = float(temperature_dallas)

    if OUTPUT_INFOFILE:
        write_infofile(temperature_data)
    if OUTPUT_JSON:
        write_json(temperature_data)

    if tempy.update({"source": "wipi",
                     "sensor": "wipi-int",
                     "temperature": temperature_dht22,
                     "humidity": humidity_dht22}):
        print "Update was a success"
    else:
        print "Update failed"


if __name__ == '__main__':
    main()

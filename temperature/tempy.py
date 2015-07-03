import requests

tempy_url = "http://tempy.tln"


def get_last(sensor_name):
    url = "{0}/get/{1}/last".format(tempy_url, sensor_name)
    print "url:", url
    result = requests.get(url).json
    print "Debug:",result
    return result


def get_temperature(sensor_name):
    temperature_data = get_last(sensor_name)
    if "temperature" in temperature_data:
        return temperature_data["temperature"]
    return False


def get_humidity(sensor_name):
    temperature_data = get_last(sensor_name)
    if "humidity" in temperature_data:
        return temperature_data["humidity"]
    return False


def update(data):
    url = "{}/add".format(tempy_url)
    try:
        requests.post(url, data=data)
    except:
        return False
    return True

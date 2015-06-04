import requests
def update(data):
    requests.post("http://tempy.tln/add",data=data)


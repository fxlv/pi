import requests
def update(data):
    requests.post("http://tempy.tln:3000/add",data=data)


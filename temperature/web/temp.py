from flask import Flask, render_template
from azurepy import queues

app = Flask(__name__)


forecastio_queue = queues.Queue("forecastio-temperature")
ilmerree_queue = queues.Queue("ilmerree-temperature")
int_temperature_queue = queues.Queue("wipi-int-temperature")
int_humidity_queue = queues.Queue("wipi-int-humidity")


all_queues = [
    forecastio_queue, int_temperature_queue,
    ilmerree_queue]


@app.route('/')
def index():
    temperatures = []
    for queue in all_queues:
        message = queue.peek_message()
        temp = {}
        temp['name'] = queue
        temp['temperature'] = message.message_text
        temp['insertion_time'] = message.insertion_time
        temp['expiration_time'] = message.expiration_time
        temperatures.append(temp)
    humidity = int_humidity_queue.peek_message()
    return render_template(
        "index.html",
        temperatures=temperatures,
        humidity=humidity)

if __name__ == "__main__":
    app.run(debug=True)

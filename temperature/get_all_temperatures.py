#!/usr/bin/env python
#
# for testing and development purposes only
#
from azurepy import queues



forecastio_queue = queues.Queue("forecastio-temperature")
int_temperature_queue = queues.Queue("wipi-int-temperature")
int_humidity_queue = queues.Queue("wipi-int-humidity")


all_queues = [forecastio_queue, int_temperature_queue, int_humidity_queue]

def length():
    print "Lengths of all queues"
    for q in all_queues:
        print q,q.length()

def pop_last():
    for queue in all_queues:
        print "Queue: {0}".format(queue)
        message = queue.get_message()
        print message.message_text
        print message.insertion_time
        print message.expiration_time
        queue.delete_message(message)

def clear():
    forecastio_queue.clear()
    int_temperature_queue.clear()
    int_humidity_queue.clear()


if __name__ == "__main__":
    length()
    pop_last()


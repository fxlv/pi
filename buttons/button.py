import RPi.GPIO as GPIO
import time
sleep_time = 0.1


def sleep(sleep_time):
    print "Sleeping for {} seconds".format(sleep_time)
    time.sleep(sleep_time)


GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.IN)

GPIO.output(26, GPIO.HIGH)


def wait_for_button_press(button_id):
    while True:
        if (GPIO.input(button_id)):
            print "Button pressed"
        sleep(sleep_time)


if __name__ == "__main__":
    try:
        wait_for_button_press(20)
    except:
        GPIO.cleanup()

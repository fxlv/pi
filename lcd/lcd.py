#!/usr/bin/env python
#
# Control HD44780 LCD on a RaspberryPi
#
# https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
# https://en.wikipedia.org/wiki/Hitachi_HD44780_LCD_controller
#
# If you want to understand the logic behind the hex codes
# use a calculator. In binary it all makes sense.
#

import RPi.GPIO as GPIO
import time

DEBUG = True

GPIO.setmode(GPIO.BOARD)

register_select = 26  # select between command (0) or character (1)
enable = 24  # Enable data transmit

# use 4 pins for data
bit4 = 22
bit5 = 18
bit6 = 16
bit7 = 12

lcd_backlight = 29  # switches on +5v via transistor


def backlight(mode=True):
    "Set the backlight on or off"
    GPIO.output(lcd_backlight, mode)


def debugprint(msg):
    global DEBUG
    if DEBUG:
        print "DEBUG: {0}".format(msg)

pins_list = [29, 26, 24, 12, 16, 18, 22]


def set_pins_to_out(pins_list):
    for pin in pins_list:
        debugprint("Setting pin #{0} to OUT".format(pin))
        GPIO.setup(pin, GPIO.OUT)

set_pins_to_out(pins_list)


def clear_screen():
    send_cmd(0x01)


def main():
    try:
        run_test()
    except KeyboardInterrupt:
        clear_screen()
        print "Exiting..."

def write_screen(msg, display_time=5):
    """
    Display up to four line message on the screen
    msg - a list or a string, lines can be delimited with newline
    Line can be 20 chars long and there can be 4 lines or less.
    """
    empty_line = " "*20
    clear_screen()
    if isinstance(msg, str):
        msg = msg.splitlines()
    if not isinstance(msg, list):
        debugprint("write_screen() accepts only lists")
        lcd_write_line(empty_line, 1)
        lcd_write_line("Invalid message!", 2)
        lcd_write_line(empty_line, 3)
        lcd_write_line(empty_line, 4)
    else:
        if len(msg) > 4:
            debugprint("Message list too long")
            sys.exit(1)
        elif len(msg) == 0:
            debugprint("Message list empty")
            sys.exit(1)
        elif len(msg) != 4:
            # pad with empty lines if needed
            while len(msg) != 4:
                msg.append(empty_line)
        for line in msg:
            # truncate long lines
            if len(line) > 20:
                display_line = line[:17]+"..."
            else:
                display_line = line
            lcd_write_line(display_line, msg.index(line)+1)
        time.sleep(display_time)

def run_test():
    lcd_init()
    backlight()
    write_screen("kaka")
    while True:
        debugprint("test started")
        lcd_write_line("Hello", 1)
        time.sleep(2)  # 20 second delay
        lcd_write_line("World", 2)
        time.sleep(2)
        lcd_write_line("HD44780", 3)
        time.sleep(2)
        lcd_write_line("on Raspberry Pi", 4)
        time.sleep(2)
        clear_screen()
        time.sleep(1)


def lcd_init():
    send_cmd(0x33)
    send_cmd(0x32)
    send_cmd(0x28)
    send_cmd(0x0C)
    send_cmd(0x06)
    send_cmd(0x01)
# seems like a little bit of sleep is needed here
# otherwise i get garbage on the display
# guess I should have read the fine manual but oh well, this hack works
    time.sleep(0.1)


def lcd_write_line(msg, line):
    "Write string to LCD line, we are constrained by 20 char limit"
    if line == 1:
        position = 0x80
    if line == 2:
        position = 0xC0
    if line == 3:
        position = 0x94
    if line == 4:
        position = 0xD4
    if len(msg) > 20:
        msg = "Line too long!"
    else:
        msg = msg.ljust(20, " ")  # fill with whitespace up to 20 chars
    # set position for the cursor
    send_cmd(position)
    for char in msg:
        send_char(char)


def send_char(char):
    hex_char = ord(char)
    debugprint("Sending char: {0}, hex_char: {1}".format(char, hex_char))
    send(hex_char, True)


def send_cmd(cmd):
    debugprint("Sending command: {0}".format(cmd))
    send(cmd, False)


def data_off():
    " Set the data pins off "
    GPIO.output(bit4, False)
    GPIO.output(bit5, False)
    GPIO.output(bit6, False)
    GPIO.output(bit7, False)


def send(data, mode):
    """
    data - command or characters
    mode - boolean, register_select mode
    """
    if mode:
        debugprint("Sending characters")
    else:
        debugprint("Sending command")
    debugprint("Sending: {0}".format(data))
    GPIO.output(register_select, mode)

    # switch all pins off
    data_off()

    # 0001 0000
    if data & 0x10 == 0x10:
        GPIO.output(bit4, True)
    # 0010 0000
    if data & 0x20 == 0x20:
        GPIO.output(bit5, True)
    # 0100 0000
    if data & 0x40 == 0x40:
        GPIO.output(bit6, True)
    # 1000 0000
    if data & 0x80 == 0x80:
        GPIO.output(bit7, True)

    # tell lcd to read data
    enable_command()

    # switch all pins off
    data_off()

    # 0000 0001
    if data & 0x01 == 0x01:
        GPIO.output(bit4, True)
    # 0000 0010
    if data & 0x02 == 0x02:
        GPIO.output(bit5, True)
    # 0000 0100
    if data & 0x04 == 0x04:
        GPIO.output(bit6, True)
    # 0000 1000
    if data & 0x08 == 0x08:
        GPIO.output(bit7, True)

    # tell lcd to read data
    enable_command()


def enable_command():
    "Send a HIGH pulse to the Enable pin"
    time.sleep(0.00005)
    GPIO.output(enable, True)
    time.sleep(0.00005)
    GPIO.output(enable, False)


if __name__ == '__main__':
    main()

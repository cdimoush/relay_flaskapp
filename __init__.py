from flask import Flask, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

red_pin = 5
green_pin = 6
blue_pin = 13
coffee_pin = 19
amp_pin = 26
ON = 0
OFF = 1  # for some reason relay is backwards, ON or 1 means OFF


GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)  # red pin, controls 1st relay
GPIO.setup(green_pin, GPIO.OUT)  # green pin, controls 4th relay (second relay appears broken)
GPIO.setup(blue_pin, GPIO.OUT)  # blue pin, controls 3rd relay
GPIO.setup(coffee_pin, GPIO.OUT)  # coffee pin, controls 5th relay
GPIO.setup(amp_pin, GPIO.OUT)  # amp pin, controls 6th relay


@app.route('/')
def test():
    print('started on')
    return 'Home Page of 8 channel relay control'


# ############################################################ #
#                                                              #
# The following functions deal with the RGB LED light strips   #
#                                                              #
# ############################################################ #

@app.route('/red', methods=['GET', 'POST'])
def red():
    print('turning lights red')
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(red_pin, ON)
        GPIO.output(green_pin, OFF)
        GPIO.output(blue_pin, OFF)
        print('done')
    return 'red'


@app.route('/green', methods=['GET', 'POST'])
def green():
    print('turning lights green')
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(red_pin, OFF)
        GPIO.output(green_pin, ON)
        GPIO.output(blue_pin, OFF)
        print('done')
    return 'green'


@app.route('/blue', methods=['GET', 'POST'])
def blue():
    print('turning lights blue')
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(red_pin, OFF)
        GPIO.output(green_pin, OFF)
        GPIO.output(blue_pin, ON)
        print('done')
    return 'blue'


@app.route('/purple', methods=['GET', 'POST'])
def purple():
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(red_pin, ON)
        GPIO.output(green_pin, OFF)
        GPIO.output(blue_pin, ON)
        print('done')
    return 'purple'


@app.route('/white', methods=['GET', 'POST'])
def white():
    print('turning lights white')
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(red_pin, ON)
        GPIO.output(green_pin, ON)
        GPIO.output(blue_pin, ON)
        print('done')
    return 'white'


@app.route('/lights_off', methods=['GET', 'POST'])
def all_off():
    print('turning lights off')
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(red_pin, OFF)
        GPIO.output(green_pin, OFF)
        GPIO.output(blue_pin, OFF)
        print('done')
    return 'lights are off'


# ############################################################ #
#                                                              #
# The following functions deal with the coffee pot and amp     #
#                                                              #
# ############################################################ #


@app.route('/coffee_on', methods=['GET', 'POST'])
def all_off():
    print('turning coffee on')
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(coffee_pin, ON)
        print('done')
    return 'coffee on'


@app.route('/coffee_off', methods=['GET', 'POST'])
def all_off():
    print('turning coffee off')
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(coffee_pin, OFF)
        print('done')
    return 'coffee off'


@app.route('/amp_on', methods=['GET', 'POST'])
def all_off():
    print('turning amp on')
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(amp_pin, ON)
        print('done')
    return 'amp on'


@app.route('/amp_of', methods=['GET', 'POST'])
def all_off():
    print('turning amp off')
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(amp_pin, OFF)
        print('done')
    return 'amp off'


# ############################################################ #
#                                                              #
# The last two functions are for ALL Off and Emergency Off     #
#                                                              #
# ############################################################ #


@app.route('/all_off', methods=['GET', 'POST'])
def all_off():
    print('turning everything off')
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(red_pin, OFF)
        GPIO.output(green_pin, OFF)
        GPIO.output(blue_pin, OFF)
        GPIO.output(coffee_pin, OFF)
        GPIO.output(amp_pin, OFF)
        print('done')
    return 'every thing is off'


@app.route('/emergency_off', methods=['GET', 'POST'])  # This function wipes all GPIO pins
def emergency_off():
    print('program coming to an emergency stop')
    if request.method == 'POST' or request.method == 'GET':
        GPIO.output(red_pin, OFF)
        GPIO.output(green_pin, OFF)
        GPIO.output(blue_pin, OFF)
        GPIO.output(coffee_pin, OFF)
        GPIO.output(amp_pin, OFF)
        print('GPIO pin have been cleaned')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

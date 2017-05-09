from flask import Flask, request, render_template, redirect
from flask_ask import Ask, statement, question
import random

import RPi.GPIO as GPIO

print('Booting __init__.py file')

app = Flask(__name__)
ask = Ask(app, '/alexa')


''' pin order is important because lists control the GPIO pins. The order is...

 red = 0
 green = 1
 blue = 2
 coffee = 3
 amp = 4

'''

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

# The lists inside the dictionary are made for the negative logic of the relay
color_dict = {'red': [0, 1, 1], 'green': [1, 0, 1], 'blue': [1, 1, 0], 'purple': [0, 1, 0],
              'white': [0, 0, 0], 'lights_off': [1, 1, 1]}

appliance_dict = {'coffee': [0], 'coffee_off': [1], 'amp': [0], 'amp_off': [1]}
# The synonym dictionary allows for multiple inputs from Alexa, then corrects them for program
app_synonym_dict = {'coffee': ['coffee'], 'amp': ['amp', 'amplifier', 'stereo', 'speakers']}

#######################################################################################################################
#                                                                                                                     #
#                                                                                                                     #
#                     Below are Lists of Strings that Alexa will use for a variety of responses                       #
#                                                                                                                     #
#                       Also a function for selecting a response, some responses are weighted                         #
#                                                                                                                     #
#######################################################################################################################


def select_statement(intent, color, appliance):

    light_response = ['Turning lights to ' + color, 'Changing lights to ' + color, 'Good choice',
                      'Are you trying to set the mood sir?', color + ' is a very lovely color']
    gen_response = ['Yes sir.', 'On it.', 'Of course', 'Of course, if you need anything else let me know',
                    'Processing your request']
    coffee_response = ['Making coffee', 'Your coffee will be ready momentarily']
    amp_response = ['Turning amplifier on', 'Amplifier is on', 'Powering the stereo now']
    shutdown_response = ['Turning everything off', 'Talk to you later sir']
    no_response = ['I am here if you need me']
    funny_response = ['As you wish', 'Consider it done', 'I would love to', 'No worries',
                      'Yes, I am sworn to carry your burden', 'Why do I have to do all the work',
                      'How about you do something for once']
    dirty_response = ['Fuck you, but sure', 'Maybe you should get off your ass and do it yourself']

    i = random.randint(1, 100)

    # The first group of if statements determine if the response should pertain to the specific output

    if intent == 'LightIntent':
        if 0 < i <= 40:
            j = random.randint(0, len(light_response) - 1)
            response = light_response[j]
            return response
    if intent == 'ApplianceIntent_ON':
        if appliance == 'coffee':
            if 0 < i <= 40:
                j = random.randint(0, len(coffee_response) - 1)
                response = coffee_response[j]
                return response
        if appliance == 'amp':
            if 0 < i <= 40:
                j = random.randint(0, len(amp_response) - 1)
                response = amp_response[j]
                return response
    if intent == 'ApplianceIntent_OFF':
        if appliance == 'coffee':
            if 0 < i <= 40:
                j = random.randint(0, len(coffee_response) - 1)
                response = coffee_response[j]
                return response
        if appliance == 'amp':
            if 0 < i <= 40:
                j = random.randint(0, len(amp_response) - 1)
                response = amp_response[j]
                return response
    if intent == 'ShutdownIntent':
        if 0 < i <= 40:
            j = random.randint(0, len(shutdown_response) - 1)
            response = shutdown_response[j]
            return response
    if intent == 'NoIntent':
        if 0 < i <= 40:
            j = random.randint(0, len(no_response) - 1)
            response = no_response[j]
            return response

    # The second group of if statements decide if the response should be general (general, funny, dirty)

    if 40 < i <= 80:
        j = random.randint(0, len(gen_response) - 1)
        response = gen_response[j]
        return response
    if 80 < i <= 95:
        j = random.randint(0, len(funny_response) - 1)
        response = funny_response[j]
        return response
    if 95 < i <= 100:
        j = random.randint(0, len(dirty_response) - 1)
        response = dirty_response[j]
        return response

#######################################################################################################################


#######################################################################################################################
#                                                                                                                     #
#                                                                                                                     #
#          The following two functions deal with the GPIO output and controlling the 8channel relay                   #
#                                                                                                                     #
#                         Unlike the previous version request cannot be made from URL                                 #
#                                                                                                                     #
#######################################################################################################################

def get_output_type(value, output_type):

    for key in color_dict:
        if key == value:
            output_type = 'LIGHTS'
            break

    for key in appliance_dict:
        if key == value:
            output_type = 'APPLIANCE'
            break

    if value == 'all_off':
        output_type = 'SHUTDOWN'

    return output_type


def gpio_output(output_value):  # This function just prints rn, will be adjusted for gpio in real code

    output_type = get_output_type(output_value, None)  # gets type of output to simplify if statements
    print(output_value)

    if output_type == 'LIGHTS':

        print('RED --->' + str(color_dict[output_value][0]))
        print('GREEN --->' + str(color_dict[output_value][1]))
        print('BLUE --->' + str(color_dict[output_value][2]))

        GPIO.output(red_pin, color_dict[output_value][0])
        GPIO.output(green_pin, color_dict[output_value][1])
        GPIO.output(blue_pin, color_dict[output_value][2])

    if output_type == 'APPLIANCE':

        if output_value == 'coffee' or output_value == 'coffee_off':

            print('COFFEE --->' + str(appliance_dict[output_value][0]))

            GPIO.output(coffee_pin, appliance_dict[output_value][0])

        if output_value == 'amp' or output_value == 'amp_off':

            print('AMP --->' + str(appliance_dict[output_value][0]))

            GPIO.output(amp_pin, appliance_dict[output_value][0])

    if output_type == 'SHUTDOWN':

        print('TURNING EVERYTHING OFF')
        GPIO.output(red_pin, OFF)
        GPIO.output(green_pin, OFF)
        GPIO.output(blue_pin, OFF)
        GPIO.output(coffee_pin, OFF)
        GPIO.output(amp_pin, OFF)
        print('done')


#######################################################################################################################
#                                                                                                                     #
#                                                                                                                     #
#       Following functions set up homepage for the Flask Application, Ask Application, and Ask Intents               #
#                                                                                                                     #
#                        Intent functions return statements and correct for synonyms                                  #
#                                                                                                                     #
#######################################################################################################################


@app.route('/')  # Home Page of the website, displays the buttons. HTML code handles button redirect
def home():
    return render_template('home.html')


@ask.launch  # Sets up flask ask, if no intent alexa will ask for desired output
def new_ask():
    welcome = 'What would you like me to do'
    return question(welcome)


@ask.intent('LightIntent')  # This handles just the RGB LEDS. Color is passed through from Amazon
def request_light(color):
    if color == 'off':
        gpio_output('lights_off')
    else:
        gpio_output(color)
    return statement(select_statement('LightIntent', color, None))


@ask.intent('ApplianceIntent_ON')
def appliance_on(appliance):
    for key in app_synonym_dict:
        for i in range(0, len(app_synonym_dict[key])):
            if appliance == app_synonym_dict[key][i]:
                appliance = key
    gpio_output(appliance)
    return statement(select_statement('ApplianceIntent_ON', 'None', appliance))


@ask.intent('ApplianceIntent_OFF')
def appliance_off(appliance):
    for key in app_synonym_dict:
        for i in range(0, len(app_synonym_dict[key])):
            if appliance == app_synonym_dict[key][i]:
                appliance = key
    app_off = appliance + '_off'
    gpio_output(app_off)
    return statement(select_statement('ApplianceIntent_OFF', 'None', appliance))


@ask.intent('ShutdownIntent')
def shutdown():
    gpio_output('all_off')
    return statement(select_statement('Shutdown', 'None', None))


@ask.intent('NoIntent')
def no_intent():
    return statement(select_statement('NoIntent', 'None', None))

#######################################################################################################################
#                                                                                                                     #
#                                                                                                                     #
#       Only other page on Website, Button Function deals with returned values then redirects to home                 #
#                                                                                                                     #
#                                                                                                                     #
#                                                                                                                     #
#######################################################################################################################


@app.route('/button', methods=['POST', 'GET'])
def button():
    if request.method == 'POST' or 'GET':
        button_value = request.form['submit']
        gpio_output(button_value)

        return redirect('/')


@app.route('/emergency_off', methods=['GET', 'POST'])  # This function wipes all GPIO pins, acces from url
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
    GPIO.output(red_pin, OFF)
    GPIO.output(green_pin, OFF)
    GPIO.output(blue_pin, OFF)
    GPIO.output(coffee_pin, OFF)
    GPIO.output(amp_pin, OFF)
    print('Flask Application Started, all PINs are off')
    app.run(host='0.0.0.0', port=80)

#!/usr/bin/env python3

from flask import Flask, request, jsonify

import RPi.GPIO as gpio
import time
import datetime
import atexit
import os
from cryptography.fernet import Fernet
import logging
logging.basicConfig(filename='/home/pi/doorbell/logs/door.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

up_doorbell = None
down_doorbell = None

encryption_key = None

class Relay(object):
    def __init__(self, pin=8, name=''):
        self.pin = pin
        gpio.setup(self.pin, gpio.OUT)
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.turn_off()
        atexit.register(self.turn_off)
    
    def turn_on(self, duration=None):
        gpio.output(self.pin, False)
        self.logger.info('Open door with duration {}'.format(duration))
        if duration is not None:
            time.sleep(duration)
            self.turn_off()

    def turn_off(self):
        self.logger.info('Turning off')
        gpio.output(self.pin, True)

app = Flask('doorbell')

def validate_token(token):
    logging.info("Trying token {}".format(token))
    cipher_suite = Fernet(encryption_key)
    dt = cipher_suite.decrypt(token.encode()).decode()
    dt = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.datetime.now()
    return dt > now

@app.route('/open', methods=['POST'])
def open_door():
    print(request.form)
    
    if 'token' not in request.form or not validate_token(request.form['token']):
        return "Fail - invalid token"

    if request.form['role'] == 'updoorbell':
        try:
            duration = max(0,min(float(request.form['duration']),5))
            up_doorbell.turn_on(duration)
            return 'Success'
        except:
            return 'Fail'
    elif request.form['role'] == 'downdoorbell':
        try:
            duration = max(0,min(float(request.form['duration']),5))
            down_doorbell.turn_on(duration)
            return 'Success'
        except:
            return 'Fail'
    else:
        return "Fail - incorrect form"

@app.route('/token', methods=["GET"])
def generate_token():
    now = datetime.datetime.now()+datetime.timedelta(seconds=10)
    cipher_suite = Fernet(encryption_key)
    cipher_text = cipher_suite.encrypt(str(now).encode()).decode()
    return jsonify({"token": cipher_text})

if __name__ == '__main__':
    down_doorbell = Relay(8, name='downstairs')
    up_doorbell = Relay(10, name='upstairs')

    port = None
    try:
        port = os.environ['LOCAL_PORT']
    except:
        pass

    if port is None:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path='./env')
        port = os.environ['LOCAL_PORT']
    
    encryption_key = os.environ['ENCRYPTION_KEY']

    app.run(host="127.0.0.1",port=port,debug=False)


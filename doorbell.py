#!/usr/bin/env python3

from flask import Flask, request

import RPi.GPIO as gpio
import time
import atexit
import os
import logging
logging.basicConfig(filename='/home/pi/doorbell/logs/door.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

up_doorbell = None
down_doorbell = None

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

@app.route('/', methods=['GET', 'POST'])
def do_everything():
    if request.method == 'POST':
        print(request.form)
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
        return 'Doorbell'

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
        from pathlib import Path
        load_dotenv(dotenv_path=Path('.') / 'env')
        port = os.environ['LOCAL_PORT']

    app.run(port=port)


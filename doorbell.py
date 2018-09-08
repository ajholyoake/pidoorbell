#!/usr/bin/env python3

from flask import Flask, request

import RPi.GPIO as gpio
import time
import atexit
import os

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

doorbell = None

class Relay(object):
    def __init__(self, pin=8):
        self.pin = pin
        gpio.setup(self.pin, gpio.OUT)
        self.turn_off()
        atexit.register(self.turn_off)
    
    def turn_on(self, duration=None):
        gpio.output(self.pin, False)
        if duration is not None:
            time.sleep(duration)
            self.turn_off()

    def turn_off(self):
        gpio.output(self.pin, True)

app = Flask('doorbell')

@app.route('/', methods=['GET', 'POST'])
def do_everything():
    if request.method == 'POST':
        print(request.form)
        if request.form['role'] == 'doorbell':
            duration = max(float(request.form['duration']),5)
            doorbell.turn_on(duration)
        return 'Success'
    else:
        return 'Doorbell'

if __name__ == '__main__':
    doorbell = Relay(8)
    
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


# -*- coding: utf-8 -*-
"""
Created on Sat May 18 00:22:24 2019

@author: siddharth
"""

from flask import Flask
import time
app = Flask(__name__)


@app.route('/test1')
def hello():
    time.sleep(200)
    return "Hello World!"

@app.route('/test2')
def hello2():
    time.sleep(200)
    return "Hello World!"


@app.route('/test3')
def hello3():
    time.sleep(200)
    return "Hello World!"


@app.route('/test4')
def hello4():
    return "Hello World!"



if __name__ == '__main__':
    app.run()
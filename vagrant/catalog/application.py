#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, rediect, jsonify, url_for
from flask import make_response
import httplib2
import string
import random

app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8000)

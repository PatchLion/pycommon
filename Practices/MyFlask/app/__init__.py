# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
app = Flask(__name__)
app.config['SECRET_KEY'] = 'e10812cd-09ca-4963-80c8-f9b6a0463eac'
bootstrap = Bootstrap(app)
moment = Moment(app)
from .views import *
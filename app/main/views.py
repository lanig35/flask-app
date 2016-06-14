#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import current_app
from flask_babel import gettext

from .. import babel

from . import main

@babel.localeselector
def get_locale():
    return 'es'

@main.route ('/')
def index():
    current_app.logger.info ('request')
    return gettext(u'Hello World!')


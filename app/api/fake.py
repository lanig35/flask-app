#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_babel import gettext

from . import api

@api.route ('/fake')
def index():
    return gettext(u'Hello API!')

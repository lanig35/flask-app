#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_babel import gettext
from flask import abort

from . import api

@api.route ('/users', methods=['GET'])
def get_users():
    return gettext(u'Hello API!')

@api.route ('/users/1', methods=['GET'])
def users ():
    abort (403)

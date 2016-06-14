#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import jsonify

from . import api

@api.errorhandler (403)
def not_found (e):
    response = jsonify ({'error': 'forbidden'})
    response.status_code = 403
    return response 

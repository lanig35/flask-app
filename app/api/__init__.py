#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

api = Blueprint ('api', __name__)

from . import fake, users, errors

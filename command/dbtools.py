#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import current_app
from command import database

@database.command
def create ():
    "create a new db"
    pass

@database.command
def delete (db=None):
    "delete a db"
    pass

@database.option ('-f', '--format', dest='f', choices=['j', 't'])
def fake (f):
    "fate command"
    pass

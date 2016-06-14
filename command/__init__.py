#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_script import Manager

database = Manager (usage='CouchDB utilities')
populate = Manager (usage='utilities to generate fake data',
                    description='allow to populate db with test data')

import dbtools, gentools 

#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import current_app
from faker import Faker
from command import populate 

import requests
import json

@populate.option ('-c', '--count', dest='count', metavar='n', type=int, default=5, help='number of users to create')
def user (count):
    "generate a set of users"
    fake = Faker ('fr_FR')
    for i in range (0, count):
        data = fake.simple_profile ()
        item = {
            'type': 'user',
            'name': data['username'],
            'password': 'reverse',
            'mail': data['mail'],
            'roles': [],
        }

        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        url = 'http://127.0.0.1:5984/_users/org.couchdb.user:' + item['name']
        r = requests.put (url, headers=headers, data=json.dumps (item))
        print r.status_code, r.text

@populate.option ('-c', '--count', dest='count', metavar='n', type=int, default=5, help='number of books to create')
@populate.option (dest='db', metavar='db-name', help='Name of the database')
def book (db, count):
    "generate a set of books"
    fake = Faker ('fr_FR')
    dataset = []
    for i in range (0, count):
        item = {
            'author': fake.name_male (),
            'title': fake.sentence (nb_words=3),
            'publisher': fake.company (),
            'description': fake.text (),
            'publishedDate': fake.year ()
        }
        dataset.append (item)

    headers = {'Content-Type': 'application/json'}
    url = 'http://127.0.0.1:5984/' + db + '/_bulk_docs'
    payload = {'docs': dataset}
    r = requests.post (url, headers=headers, data=json.dumps (payload))
    print r.status_code, r.text

@populate.option ('-c', '--count', dest='count', metavar='n', type=int, default=5, help='number of authors to create')
@populate.option (dest='db', metavar='db-name', nargs=1, help='Name of the database')
def author (db, count):
    "generate a set of authors"
    pass


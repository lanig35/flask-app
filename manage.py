#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
os.environ['APP_CONFIG_FILE'] = '/home/ec2-user/training/config/default.py'

import logging
from logging.handlers import RotatingFileHandler

from flask import current_app
from flask_script import Manager
from app import app

import json
import requests
from prettytable import PrettyTable

# mise en place journalisation
handler = RotatingFileHandler (app.config['LOG_FILE'],
                               maxBytes=app.config['LOG_BYTES'],
                               backupCount=app.config['LOG_COUNT'])
formatter = logging.Formatter ('%(asctime)s-%(levelname)s [%(module)s-%(funcName)s]: %(message)s')

handler.setFormatter (formatter)
handler.setLevel (app.config['LOG_LEVEL'])

# attachement du module de log
app.logger.addHandler (handler)

# creation du manager
manager = Manager (app)

# mise en place des commandes simples
@manager.command
def check (msg='all right!'):
    "helper function to see if flask script in place"
    current_app.logger.info ('hello')
    print 'Message: ', msg

@manager.command
def secret ():
    "Generate a new private key"
    current_app.logger.info ('secret')
    print os.urandom(24).encode('hex')

@manager.option ('-f', '--format', dest='format', choices=['json', 'table'], default='json', help='how to format the output')
@manager.option ('-c', '--count', dest='count', metavar='n', type=int, default=5, help='max number of items to return')
@manager.option ('-l', '--language', dest='lang', choices=['fr', 'en', 'es'], default='fr', help='language for the search')
@manager.option ('-t', '--title', dest='title', required=False, metavar='word', help='word from the title')
@manager.option (dest='author', nargs='+', help='Name of the author')
def lookup (format, count, lang, title, author):
    "lookup for books in the Google book database"
    # construction du critère de recherche
    q = 'inauthor:'+'+'.join(author)
    if title is not None:
        q = q + '+intitle:'+title

    # parametre de la recherche
    payload = {
        'key': current_app.config['GBOOK_KEY'],
        'projection': 'lite',
        'langRestrict': lang,
        'prettyPrint': False,
        'maxResults': count,
        'fields': 'totalItems,items(etag,id,volumeInfo/title,volumeInfo/authors,volumeInfo/publisher,volumeInfo/publishedDate)',
        'q': q
    }

    current_app.logger.info ('{0} - lang={1} output={2} count={3}'.format (q, lang, format, count))

    r = requests.get (current_app.config['GBOOK_API'], params=payload)
    if r.status_code != 200:
        response = {'code': r.status_code, 'reason': r.json()['error']['message']}
        current_app.logger.error (response)
        return json.dumps(response, indent=2)

    table = PrettyTable (['#', 'Titre', 'Editeur', 'Auteur', 'PubDate', 'id'])
    data = []
    count = 1

    if r.json()['totalItems'] > 0:
        for item in r.json()['items']:
            data.append ( 
                {
                    'id': item['id'],
                    'titre': item['volumeInfo']['title'],
                    'auteur': item['volumeInfo']['authors'],
                    'editeur': item['volumeInfo'].get('publisher','inconnu'),
                    'pubDate': item['volumeInfo']['publishedDate'].split('-')[0]
                }
            )
            info = item['volumeInfo']
            pubdate =  info['publishedDate'].split('-')[0]
            table.add_row ([count, info['title'], info.get('publisher', 'inconnu'), info['authors'][0], pubdate, item['id']])
            count+=1

    if format == 'json':
        sortie = {
            'total': r.json()['totalItems'],
            'count': count,
            'items': data
        }
        return json.dumps (sortie, indent=2)

    if format == 'table':
        return table

# mise en place des commandes groupees
from command import database, populate 
manager.add_command ('database', database)
manager.add_command ('fake', populate)

if __name__ == "__main__":
    # lancement du programme
    manager.run ()


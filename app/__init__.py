#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_babel import Babel

# creation de l'application
app = Flask (__name__, instance_relative_config=True)

# chargement de la configuration
# 1 - par defaut (racine config)
# 2 - pour l'instance (repertoire instance)
# 3 - selon la variable d'environnement si presente
# chaque niveau ecrase le precedent si meme variable
app.config.from_object ('config.default')
app.config.from_pyfile ('config.py')
app.config.from_envvar('APP_CONFIG_FILE')

# creation et enregistrement des extensions
babel = Babel (app)

# creation du blueprint principal
from .main import main
app.register_blueprint (main)

# creation du blueprint API
from .api import api
app.register_blueprint (api, url_prefix='/api')

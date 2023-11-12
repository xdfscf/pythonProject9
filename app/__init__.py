from flask import Flask
from flask_migrate import Migrate
import flask
import logging
import os

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_POOL_SIZE'] = 60
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import views,models


from flask import Flask

app = Flask(__name__)

app.config.from_object('secret_config')

from app import views
from app import api
from app import config

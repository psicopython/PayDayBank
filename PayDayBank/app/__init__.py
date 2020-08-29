from .confg import config_geral
from .model import config_dbase
from .views import config_views

from flask import Flask



def create():
	app = Flask(__name__)
	
	config_geral(app)
	config_dbase(app)
	config_views(app)
	
	return app
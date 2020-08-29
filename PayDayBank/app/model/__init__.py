from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate


db = SQLAlchemy()
mi = Migrate()



def config_dbase(app):
	db.init_app(app)
	app.db = db
	
	mi.init_app(app,app.db)
	

from . import user
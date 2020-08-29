


def config_geral(app):
	app.config["SECRET_KEY"] = 'FuScAzUL'
	app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///dbase.db'
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.template_folder = 'front/templates/'
	app.static_folder = 'front/static/'
	

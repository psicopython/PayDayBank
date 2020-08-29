from flask import Blueprint



from .home import index
from .validar import validacaoEredefinicao
from .login import login, logout
from .criar_conta import criar_conta



# Instanciando Um objeto Blueprint
bp = Blueprint(
	'webui',  # Web User Interface : as views do programa
	__name__, # Name da pasta principal
)

# Rota index
bp.add_url_rule(
	'/',
	methods=['GET','POST'],
	view_func=index,
	endpoint="index",
)

# Rota Cadastro de usuários
bp.add_url_rule(
	'/criar_conta/',
	methods=['GET','POST'],
	view_func=criar_conta,
	endpoint="criar_conta",
)

bp.add_url_rule(
	'/login/',
	methods=['GET','POST'],
	view_func=login,
	endpoint="login",
)

bp.add_url_rule(
	'/logout/',
	methods=['GET','POST'],
	view_func=logout,
	endpoint="logout",
)

bp.add_url_rule(
	'/validacao/<string:token>/',
	methods=['GET','POST'],
	view_func=validacaoEredefinicao,
	endpoint="validacaoEredefinicao",
)



def config_views(app):
	app.register_blueprint(bp)
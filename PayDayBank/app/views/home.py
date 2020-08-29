

from flask import (
	render_template,session,abort,
	request,jsonify,redirect,
)

from app.auth import auth
from app.email import validaEmail
from .validar import valCpf

@auth(session)
def index(user):
	if not user.val_email:
		a = validaEmail(user)
		if a:
			return a
		
	print(valCpf(user.getJson()['cpf']))
	return jsonify(user.getJson())
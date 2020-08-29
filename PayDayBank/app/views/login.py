

from app.auth import (
	Atum, auth2,
)

from app.model.user import (
	User
)

from flask import (
	render_template, request, redirect,
	jsonify, abort, current_app, session,
)

from datetime import datetime, timedelta, date


@auth2(session)
def login():
	data, JS = {}, False
	if request.method == 'POST':
		if request.form:
			data['usuario'] = request.form['usuario']
			data['senha']   = request.form['senha']
			
		elif request.json:
			data = request.json['user']
			JS = True
	
		user = User.query.filter_by(email=data['usuario']).first()
		if user:
			if user.check_senha(data['senha']):
				
				chave = Atum.encrypt(bytes(f'{user.id}/{user.email}/{date.today()}/{date.today() + timedelta(1200)}/{user.chave}','utf-8'))
				session['bacalhau'] = chave
				
				return jsonify('ok'),200
			else:
				return abort(401)
		else:
			return abort(404)
		
	elif request.method == 'GET':
		return render_template('login.html')
		
	else:
		abort(404)
	

def logout():
	session.pop('bacalhau',None)
	return redirect('/login/')
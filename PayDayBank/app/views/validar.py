
from app.auth import Atum, auth

from app.model.user import User

from flask import (
	session, current_app,
	redirect, abort
)


def validacaoEredefinicao(token):
	# token "/{user.id}/{user.chave}/{user.email}/{opt:email}/"
	origin_token = token
	token = Atum.decrypt(bytes(token,'utf-8')).decode("utf-8")
	token = token.split('/')
	
	user = User.query.filter_by(id=token[0]).first()
	if user:
		if user.val_email:
			return '<center><h1>token Inválido</h1></center>'
			#abort(404)
		if user.getJson()['email'] == token[2]:
			
			if token[3] == 'email':
				if user.chave == token[1]:
					User.query.filter_by(id=user.id).update({'val_email': True })
					current_app.db.session.commit()
					return redirect('/')
					
			elif token[3] == 'senha':
				return render_template('senha.html',token=origin_token)
	return abort(404)



def valCpf(cpf):
	if len(cpf) == 14:
		cpf = cpf.replace('.','').replace('-','')
		val1, val2, cont= 0, 0, 10
		
		for c in range(0,10):
			c = str(c)
			a = [c,c,c,c,c,c,c,c,c,c,c]
			if list(cpf) == a:
				return False
				
		for i in cpf[:9]:
			val1 += int(i) * cont 
			cont -= 1
		cont = 11
		
		for i in cpf[:10]:
			val2 += int(i) * cont
			cont -= 1
				
		val1 = (val1 * 10)%11
		val2 = (val2 * 10)%11
		
	
		if val1 == int(cpf[9]) and val2 == int(cpf[10]):
			return True
	return False
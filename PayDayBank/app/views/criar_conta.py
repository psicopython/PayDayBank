
from app.model.user import User, Conta
from app.email import validaEmail
from app.auth import Atum, auth2
from .validar import valCpf

from datetime import timedelta, date, datetime
from requests import post

from flask import (
	current_app, url_for, flash,
	request, redirect, abort,
	render_template, jsonify,
	session,
)



@auth2(session)
def criar_conta():
	if request.method == 'POST':
		data, JS, campoVazio, campoInvalido = {}, False, [], []
		if request.json:
			data = request.json['user']
			JS = True
		elif request.form:
			
			data['rg'] = request.form['rg']
			data['cpf'] = request.form['cpf']
			data['num'] = request.form['num'] # n° da casa
			data['cep'] = request.form['cep']
			data['nome'] = request.form['nome']
			data['email'] = request.form['email']
			data['senha'] = request.form['senha']
			data['senha2'] = request.form['senha2']
			data['cidade'] = request.form['cidade']
			data['estado'] = request.form['estado']
			data['endereco'] = request.form['endereco']
			data['sobrenome'] = request.form['sobrenome']
			data['data_nasc'] = request.form['data_nasc']
		
		if not data['rg']:
			campoVazio.append('RG')
			
		if not data['cpf']:
			campoVazio.append('CPF')
			
		if not valCpf(data['cpf']):
			campoInvalido.append('CPF inválido')
			
		if not data['nome']:
			campoVazio.append('NOME')
			
		if not data['data_nasc']: 
			campoVazio.append('DATA DE NASCIMENTO')
			
		if not data['sobrenome']:
			campoVazio.append('SOBRENOME')
			
		if not data['num']:
			campoVazio.append('NUMERO')
			
		if not data['cep']:
			campoVazio.append('CEP')
			
		if not ['endereco']:
			campoVazio.append('ENDEREÇO')
			
		if not data['cidade']:
			campoVazio.append('CIDADE')
			
		if not data['estado']:
			campoVazio.append('UF')
			
		if not data['email']:
			campoVazio.append('EMAIL')
			
		if not data['senha']:
			campoVazio.append('SENHA')
			
		if not data['senha2']:
			campoVazio.append('CONFIRME A SENHA')
			
		if data['senha'] != data['senha2']:
			campoInvalido.append('AS SENHAS NÃO COINCIDEM ')
			
		
		if campoInvalido:
			if JS:
				return jsonify(campoInvalido),200
			else:
				flash(campoInvalido)
				return render_template
		if campoVazio:
			if JS:
				errors = None
				if campoVazio < 2:
					errors = f'O campo {campoVazio[0]} não pode ficar vazio'
				else :
					errors = f'Od campos {err+", " for err in campoVazio} não podem ficar vazio'
				
				return jsonify(errors), 200
				
			else:
				if len(campoVazio) > 1:
					flash(f'Os campos {err+"," for err in campoVazio}  não podem ficar vazio')
				else:
					flash(f'O campo {campoVazio[0]} não pode ficar vazio')
				return render_template('cadastro.html')
			
		
		val_rg = User.query.filter_by(rg=data['rg']).first()
		val_cpf = User.query.filter_by(cpf=data['cpf']).first()
		val_email = User.query.filter_by(email=data['email']).first()
		
		if not val_cpf and not val_rg and not val_email:
			user = User(
				nome=['nome'], 
				sobrenome=['sobrenome'],
				cidade=['cidade'],
				n_casa=['num'],
				cep=['cep'],
				complemento=data['complemento'],
				uf=data['estado'], 
				end=data['endereco'],
				email=data['email'],
				senha=data['senha'],
				cpf=data['cpf'],
				rg=data['rg'],
				data_nasc=datetime.strptime(data['data_nasc'],"%Y-%m-%d"), 
			)
			
			conta = Conta(user.cpf)
			
			current_app.db.session.add_all([user, conta])
			current_app.db.session.commit()
			
			
			chave = Atum.encrypt(bytes(f'{user.id}/{user.email}/{date.today()}/{date.today() + timedelta(1200)}/{user.chave}','utf-8'))
			session['bacalhau'] = chave
			
			res = validaEmail(user)
			if res:
				print(res)
				
			if JS:
				return jsonify('ok'),201
				
			return redirect(url_for('webui.index')),201
			
		
		else:
			if JS:
				return jsonify(f'{"CPF" if val_cpf else "RG" if val_rg else "EMAIL"} Ja cadastrado em nossos banco de dados'),200
			
			else:
				flash(f'{"CPF" if val_cpf else "RG" if val_rg else "EMAIL"} Ja cadastrado em nossos banco de dados'),200
				return render_template('cadastro.html')
			
		
		
	elif request.method == 'GET':
		return render_template('cadastro.html')
	
	
	else:
		abort(404)



from app.model.user import User
from app.auth import Atum, auth

from datetime import datetime
from flask import request, session

import smtplib


hora_atual = datetime.now()
lacoste = b'gAAAAABfSIg7H6EOWRnZxQ5ixxyp3QC6_5eRCn6ZZ1SFS0wdTDh4XHcTepQtQ9xiKoh6lNUqVO5yOZ-HLzNsj3YnMSTB-tAXHZbtEGh0zamilSvcvbJ0ViA='
gmail_user = 'bancopayday@gmail.com'
gmail_password = Atum.decrypt(lacoste).decode('utf-8')



@auth(session)
def validaEmail(user,*args):
	uJ = user.getJson()
	
	to = uJ['email']
	
	token = f"{user.id}/{user.chave}/{uJ['email']}/email"
	
	email_text = f"""
	De:   {gmail_user}
	Para: {uJ['email']}
	
	Assunto: Ativacao do email
	{str(request.url)}validacao/{Atum.encrypt(bytes(token,"utf-8")).decode("utf-8")}
	"""
	
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		print('ok', gmail_user, to, email_text)
		server.sendmail(gmail_user, to, email_text)
		server.close()
		return False # Não deu erro (=> deu certo)
		
	except Exception as e:
		return str(e)
	
	
def mudarSenha(email:str):
	user = User.query.filter_by(email=email).first()
	uJ = user.getJson()
	
	token = f"{user.id}/{user.chave}/{uJ['email']}/senha"

	body  = f"{str(request.url)}validacao/{Atum.encrypt(bytes(token,'utf-8')).decode('utf-8')}/ "
	
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.sendmail(gmail_user, uJ['email'], body)
		server.close()
		return False # Não deu erro (igual a deu certo)
		
	except Exception as e:
		return str(e)
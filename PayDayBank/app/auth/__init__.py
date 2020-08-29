
from cryptography.fernet import Fernet

Atum = Fernet(b'URlNbWzc1coWZp4GwrX_eAqMnabDk35aAJsRHjYpU0I=')
Bacon = Fernet(b'b8_GvRMyq24IYXz_T032CycqJwcpdi8x2D3E_SfRW3g=')


from flask import (
	session, redirect,
	request, render_template,
)



def auth(session,*args):
	def wrapper(func):
		from app.model.user import User
		
		def valUser(*args,token=False):
			if 'bacalhau' in session:
				user_data = (
					Atum.decrypt(session['bacalhau']).decode('utf-8')
					).split('/')
					
				user = User.query.filter_by(id=user_data[0]).first()
				if user:
					if user.getJson()['email'] == user_data[1]:
						return func(user,*args)
						
				session.pop("bacalhau")
					
			return redirect('/login/')
				
		return valUser
	return wrapper


def auth2(session):
	def wrapper_2(func):
		from app.model.user import User
		def valUser_2():
			if 'bacalhau' in session:
				user_data = (
					Atum.decrypt(session['bacalhau']).decode('utf-8')
					).split('/')
					
				user = User.query.filter_by(id=user_data[0]).first()
				if user.getJson()['email'] == user_data[1]:
					return redirect('/')
				else:
					session.pop('bacalhau')
					return func()
					
			return func()
				
		return valUser_2
	return wrapper_2
	


from . import db

from datetime import datetime
from app.auth import Bacon

from werkzeug.security import (
	generate_password_hash as gph,
	check_password_hash as cph,
)

import random, string



class User(db.Model):
	
	__tablename__='user'
	
	id = db.Column(db.Integer, primary_key=True) 

	nome = db.Column(db.Unicode,nullable=False)
	sobrenome = db.Column(db.Unicode, nullable=False)
	cpf = db.Column(db.String(14), unique=True, nullable=False)
	rg = db.Column(db.Unicode, nullable=False)
	data_nasc = db.Column(db.DateTime, nullable=False)
	
	data_conta = db.Column(db.DateTime, nullable=False)

	email = db.Column(db.String(64), unique=True, nullable=False)
	val_email = db.Column(db.Boolean, nullable=False)
	
	chave = db.Column(db.String(32), nullable=False)
	senha = db.Column(db.String(256), nullable=False)
	
	cidade = db.Column(db.Unicode, nullable=False)
	estado = db.Column(db.Unicode, nullable=False)
	endereco = db.Column(db.Unicode, nullable=False)
	num = db.Column(db.Unicode, nullable=False)
	cep = db.Column(db.Unicode, nullable=False)
	complemento = db.Column(db.Unicode)
	
	
	def _get_data(self):
		return datetime.now()
	
	
	def encrypt(self, arg):
		return Bacon.encrypt(bytes(arg, 'utf-8'))
		
	def decrypt(self, arg):
		return Bacon.decrypt(arg).decode('utf-8')
	
	def ger_senha(self, arg):
		return gph(arg)
		
	def check_senha(self, senha):
		return cph(self.senha, senha)
	
	
	
	def __init__(self, nome, sobrenome, cpf, rg,
				data_nasc, cidade, uf, end, n_casa,
				cep, complemento, email, senha,):
					
		self.nome = self.encrypt(nome)
		self.sobrenome = self.encrypt(sobrenome)
		
		self.cpf = cpf
		self.rg = rg
		self.data_nasc = data_nasc
		
		self.data_conta = self._get_data()
		
		self.email = email
		self.val_email = False
		self.senha = self.ger_senha(senha)
		
		self.chave = ''.join(
				random.choice(
					string.ascii_uppercase + string.ascii_lowercase + string.digits
				) for _ in range(16)
			)
		
		self.cep = self.encrypt(cep)
		self.num = self.encrypt(n_casa)
		self.estado = self.encrypt(uf)
		self.cidade = self.encrypt(cidade)
		self.endereco = self.encrypt(end)
		self.complemento = self.encrypt(complemento)
		
	
	def getJson(self):
		return {
			
			"rg": self.rg,
			"cpf": self.cpf,
			"nascimento": self.data_nasc.strftime("%d/%m/%Y"),
			
			
			"nome": self.decrypt(self.nome),
			"sobrenome": self.decrypt(self.sobrenome),
			
			"email": self.email,
			"email_validado": self.val_email,
			
			"data_conta": self.data_conta.strftime("%d/%m/%Y as %H:%M"),
			"conta": (Conta.query.filter_by(user=self.cpf).first()).getJson(),
			
			"cep": self.decrypt(self.cep),
			"uf":  self.decrypt(self.estado),
			"numero": self.decrypt(self.num),
			"cidade": self.decrypt(self.cidade),
			"endereco": self.decrypt(self.endereco),
			"complemento": self.decrypt(self.complemento),
		}
		
	def getItems(self,args:list) -> dict:
		if args:
			response = {}
			user = self.get_user()
			for item in args:
				if item in user:
					if item != 'senha':
						response[item] = user[item]
				else:
					response[item] = 'not found'
			return response
		else:
			return False

class Conta(db.Model):
	
	__tablename__='conta'
	
	id = db.Column(db.Integer, primary_key=True) 
	conta = db.Column(db.String(11),nullable=False)
	user  = db.Column(db.String(11), unique=True,nullable=False)
	agencia = db.Column(db.String(11), nullable=False)
	saldo = db.Column(db.Unicode, nullable=False)
	
	
	def encrypt(self,arg):
		return Bacon.encrypt(bytes(str(arg),'utf-8'))
	
	def decrypt(self,arg):
		return Bacon.decrypt(arg).decode('utf-8')
	
	
	def __init__(self,us):
		self.user = us
		self.saldo = self.encrypt(0)
		self.conta = '0000000001'
		self.agencia = '0001'
		
		
	def getJson(self):
		return {
			'conta': self.conta,
			'agencia': self.agencia,
			'saldo': float(self.decrypt(self.saldo)),
		}
	


class Extrato(db.Model):
	
	__tablename__='extrato'
	
	#tipo de transferência
	tt = ['debito','credito','tranferencia','pagamento',]
	
	id = db.Column(db.Integer, primary_key=True)
	c_entrada = db.Column(db.String(16), nullable=False)
	c_saida = db.Column(db.Unicode, nullable=False)
	tipo = db.Column(db.Unicode, nullable=False)
	desc = db.Column(db.Unicode, nullable=False)
	data = db.Column(db.DateTime,nullable=False)
	valor = db.Column(db.Unicode, nullable=False)
	
	
	def encrypt(self,arg):
		return Bacon.encrypt(bytes(arg,'utf-8'))
	
	def decrypt(self,arg):
		return Bacon.decrypt(arg).decode('utf-8')
	
	
	def _get_data(self):
		return datetime.now()
	
	
	def __init__(self, ce, cs, tp, dc, vl):
		
		self.c_entrada = ce 
		self.c_saida = cs
		self.tipo = self.encrypt(tp)
		self.desc = self.encrypt(desc)
		self.valor = self.encrypt(vl)
		self.data = self._get_data()
		
	
	def getJson(self):
		return {
			'c_entrada':self.c_entrada,
			'c_saida': self.decrypt(self.c_saida),
			'tipo': tt[self.decrypt(self.tipo)],
			'desc': self.decrypt(self.desc),
			'valor': self.decrypt(self.valor),
			'data': self.data.strftime("%d %m %y as %H:%M"),
		}
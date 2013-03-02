# coding: utf-8

import socket
import threading
import time
import exceptions
import pickle
from Crypto.Util import randpool
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

ip = '10.3.1.50'
PORT_CLIENTE = 6666
PORT_SERVER_DOMAIN = 8888
PORT_SERVER_OPERATION = 7777
K = ""

#Utilizando criptografia Simétrica.
chave = 'titicadegalinhas'
cifra = AES.new(chave, AES.MODE_ECB)

#Utilizando criptografia Assimétrica.
blah = randpool.RandomPool()
private = RSA.generate(1024, blah.get_bytes)
public = private.publickey()

def busca_operacao(cabecalho, ipServidor):
	socketOperacao=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		socketOperacao.settimeout(1)
		cabecalho = string_size16(cabecalho)
		socketOperacao.sendto(cabecalho, (ipServidor, PORT_SERVER_DOMAIN))
		ipOperacao, dadosServer = socketOperacao.recvfrom(1024)
		ipOperacao = cifra.decrypt(ipOperacao)
	except:		
		return "ServidorOFF", "nada"
	socketOperacao.close()

	return ipOperacao, dadosServer

def string_size16(frase):
	parar = False
	cont = len(frase)
	while not parar :
		cont += 1
		if cont == 15:
			parar = True
		frase += " "

	return frase

def soma_prod(op, a, b, ipOperacao, dadosServer):
	print 'Servidor de Operacoes = ', ipOperacao, ' Dados do Servidor = ', dadosServer
	cabecalho = op + " {0} {1}".format(a,b)
	try: 
		socketOP=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		socketOP.settimeout(2)
		socketOP.sendto(pickle.dumps(public), (ipOperacao, PORT_SERVER_OPERATION))
		chaveSer, dadosServer = socketOP.recvfrom(2048)
		publicSer = pickle.loads(chaveSer)
		cabecalho = publicSer.encrypt(cabecalho, 32)
		socketOP.sendto(cabecalho[0], (ipOperacao, PORT_SERVER_OPERATION))		
		operacao, dadosServer = socketOP.recvfrom(2048)
		operacao = private.decrypt(operacao)
		print "\nResultado da operacao de {0} com {1} = {2} {3}".format(a,b,operacao,dadosServer)
		socketOP.close()
	except:
		print "Servidor inativo"


def op_soma(a,b,ipServidor):
	global ip,porta
	if str(a).isalpha() or str(b).isalpha():
		print "\nCaracter inválido!"
	else:
		ipOperacao, dadosServer = busca_operacao('sum', ipServidor)
		if ipOperacao == 'Bosta':
			print "Operação não encontrada na rede."
		elif ipOperacao == 'ServidorOFF' :
			print "Servidor de Nomes não está ativo!"
		else:
			soma_prod('sum', a, b, ipOperacao, dadosServer)


def op_produto(a,b,ipServidor):
	global ip,porta

	if str(a).isalpha() or str(b).isalpha():
		print "\nCaracter inválido!"
	else:
		ipOperacao, dadosServer = busca_operacao('pro', ipServidor)
		if ipOperacao == 'Bosta':
			print "Operação não encontrada na rede."
		elif ipOperacao == 'ServidorOFF':
			print "Servidor de Nomes não está ativo!"
		else:
			soma_prod('pro', a, b, ipOperacao, dadosServer)

def op_fatorial(a,ipServidor):
	global ip,porta

	if a<0:
		print "\nNão foi possível calcular o fatorial de {0}".format(a)
	elif str(a).isalpha():
		print "\nCaracter inválido!"	
	elif a==0:
		print "\nFatorial de 0 = 1"
	else:
		ipOperacao, dadosServer = busca_operacao('fat', ipServidor)
		if ipOperacao == 'Bosta':
			print "Operação não encontrada na rede."
		elif ipOperacao == 'ServidorOFF' :
			print "Servidor de Nomes não está ativo!"
		else:
			print 'Servidor de Operacoes = ', ipOperacao, ' Dados do Servidor = ', dadosServer
			cabecalho = "fat {0}".format(a)
			try:				
				socketFat=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
				socketOP.settimeout(2)
				socketFat.sendto(pickle.dumps(public), (ipOperacao, PORT_SERVER_OPERATION))
				chaveSer, dadosServer = socketFat.recvfrom(2048)
				publicSer = pickle.loads(chaveSer)
				cabecalho = publicSer.encrypt(cabecalho, 32)
				socketFat.sendto(cabecalho[0], (ipOperacao, PORT_SERVER_OPERATION))		
				operacao, dadosServer = socketFat.recvfrom(2048)
				operacao = private.decrypt(operacao)
				print "\nResultado do fatorial de {0} = {1} {2}".format(a,operacao,dadosServer)
				socketFat.close()
			except:
				print "Servidor Inativo"

			

class Operacoes:
	ipServidor = None
	def __init__(self,ipServ):
		self.ipServidor=ipServ
	
	def soma(self,a,b):
		t1=threading.Thread(target=op_soma,args=(a,b,self.ipServidor))
		t1.start()

	def produto(self,a,b):
		t2=threading.Thread(target=op_produto,args=(a,b,self.ipServidor))
		t2.start()
	
	def fatorial(self,a):
		t3=threading.Thread(target=op_fatorial,args=(a,self.ipServidor))
		t3.start()


# Acessar a classe no modo interativo:
# 	- primeiro importar: from operacoesCliente import Operacoes
#	- segundo instanciar: operacoesCliente = Operacoes('ip do servidor')
#	- terceiro usar métodos da classe: operacoesCliente.soma(5,7), operacoesCliente.produto(4,7) e operacoesCliente.fatorial(6)

# coding: utf-8

import socket
import threading
import time
import exceptions

ip = '10.3.1.50'
porta = 6666

def op_soma(a,b,ipServidor):
	global ip,porta
	socketSoma=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	try:
		socketSoma.bind((ip,porta))
	except:
		print	

	if str(a).isalpha() or str(b).isalpha():
		print "\nCaracter inválido!"
	else:
		cabecalho = "sum {0} {1}".format(a,b)
		socketSoma.sendto(cabecalho,(ipServidor,8888))
		soma, dadosServer = socketSoma.recvfrom(1024)
		print "\nResultado da Soma de {0} com {1} = {2}".format(a,b,soma)
	socketSoma.close()
	time.sleep(5)

def op_produto(a,b,ipServidor):
	global ip,porta
	socketProduto=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	
	try:
		socketSoma.bind((ip,porta))
	except:
		print

	if str(a).isalpha() or str(b).isalpha():
		print "\nCaracter inválido!"
	else:	
		cabecalho = "pro {0} {1}".format(a,b)
		socketProduto.sendto(cabecalho,(ipServidor,8888))
		produto, dadosServer = socketProduto.recvfrom(1024)
		print "\nResultado do Produto de {0} com {1} = {2}".format(a,b,produto)
	socketProduto.close()

def op_fatorial(a,ipServidor):
	global ip,porta
	socketFatorial=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	
	try:
		socketSoma.bind((ip,porta))
	except:
		print

	if a<0:
		print "\nNão foi possível calcular o fatorial de {0}".format(a)
	elif str(a).isalpha():
		print "\nCaracter inválido!"	
	elif a==0:
		print "\nFatorial de 0 = 1"
	else:
		cabecalho = "fat {0}".format(a)
		socketFatorial.sendto(cabecalho,(ipServidor,8888))
		resultado, dadosServer = socketFatorial.recvfrom(1024)
		print "\nResultado do Fatorial de {0} = {1}".format(a,resultado)
	socketFatorial.close()

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
# 	- primeiro importar: from operacoes import Operacoes
#	- segundo instanciar: operacoes = Operacoes('ip do servidor')
#	- terceiro usar métodos da classe: operacoes.soma(5,7), operacoes.produto(4,7) e operacoes.fatorial(6)

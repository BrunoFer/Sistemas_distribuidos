# coding: utf-8

import socket
import threading
import time

def op_soma(a,b,ip):
	socketSoma=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	socketSoma.bind(('10.3.1.50',8888))
	if str(a).isalpha() or str(b).isalpha():
		print "\nCaracter inválido!"
	else:	
		cabecalho = "sum {0} {1}".format(a,b)
		socketSoma.sendto(cabecalho,(ip,8888))
		soma, dadosServer = socketSoma.recvfrom(1024)
		time.sleep(5)
		print "\nResultado da Soma = ", soma
	socketSoma.close()

def op_produto(a,b,ip):
	socketProduto=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	socketProduto.bind(('10.3.1.50',7777))
	if str(a).isalpha() or str(b).isalpha():
		print "\nCaracter inválido!"
	else:	
		cabecalho = "pro {0} {1}".format(a,b)
		socketProduto.sendto(cabecalho,(ip,8888))
		time.sleep(5)
		produto, dadosServer = socketProduto.recvfrom(1024)
		print "\nResultado Produto = ", produto
	socketProduto.close()

def op_fatorial(a,ip):
	socketFatorial=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	socketFatorial.bind(('10.3.1.50',6666))
	if a<0:
		print "\nNão foi possível calcular o fatorial de {0}".format(a)
	elif str(a).isalpha():
		print "\nCaracter inválido!"	
	elif a==0:
		print "\nFatorial de 0 = 1"
	else:
		cabecalho = "fat {0}".format(a)
		socketFatorial.sendto(cabecalho,(ip,8888))
		resultado, dadosServer = socketFatorial.recvfrom(1024)
		print "\nResultado do Fatorial = ", resultado
	socketFatorial.close()

class Operacoes:
	def __init__(self,ip):
		self.ip=ip
	
	def soma(self,a,b):
		t1=threading.Thread(target=op_soma,args=(a,b,self.ip))
		t1.start()

	def produto(self,a,b):
		t2=threading.Thread(target=op_produto,args=(a,b,self.ip))
		t2.start()
	
	def fatorial(self,a):
		t3=threading.Thread(target=op_fatorial,args=(a,self.ip))
		t3.start()


# Acessar a classe no modo interativo: 
# 	- primeiro importar: from operacoes import Operacoes
#	- segundo instanciar: operacoes = Operacoes('ip do servidor')
#	- terceiro usar métodos da classe: operacoes.soma(5,7), operacoes.produto(4,7) e operacoes.fatorial(6)


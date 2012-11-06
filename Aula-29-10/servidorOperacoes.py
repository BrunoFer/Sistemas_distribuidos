# coding: utf-8

import socket
from multiprocessing import Process, Manager
import threading
import time
import exceptions

ip = '10.3.1.49'
porta = 8888

def soma(dados,dadosCliente):
	socketServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	resultado = int(dados[1])+int(dados[2])
	time.sleep(5)	
	socketServer.sendto(str(resultado),(dadosCliente[0],dadosCliente[1]))
	socketServer.close()

def produto(dados,dadosCliente):
	socketServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	resultado = int(dados[1])*int(dados[2])
	time.sleep(3)
	socketServer.sendto(str(resultado),(dadosCliente[0],dadosCliente[1]))
	socketServer.close()

def fatorialDividido(lista,a,b):
	resultado = lambda a: b if a==b else a*resultado(a-1)
	lista.append(resultado(a))

def fatorial(dados,dadosCliente):
	manager = Manager()
	lista = manager.list()
	x = int(dados[1]) 
	m1 = Process(target=fatorialDividido,args=(lista,x,x/2))
	m2 = Process(target=fatorialDividido,args=(lista,x/2-1,1))
	m1.start()
	m2.start()

	m1.join()
	m2.join()

	time.sleep(3)
	socketServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	resultFatorial=1
	for i in lista:
		resultFatorial *= i
	socketServer.sendto(str(resultFatorial),(dadosCliente[0],dadosCliente[1]))

def novaOperacao(dados,dadosCliente):
	if dados[0]=="sum":
		t1 = threading.Thread(target=soma,args=(dados,dadosCliente))
		t1.start()
	elif dados[0]=="pro":
		t1 = threading.Thread(target=produto,args=(dados,dadosCliente))
		t1.start()
	elif dados[0]=="fat":
		t1 = threading.Thread(target=fatorial,args=(dados,dadosCliente))
		t1.start()

socketServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
socketServer.bind((ip,porta))

while True:	
	dados, dadosCliente = socketServer.recvfrom(1024)
	dados = dados.split()
	print dados,dadosCliente
	t = threading.Thread(target=novaOperacao,args=(dados,dadosCliente))
	t.start()



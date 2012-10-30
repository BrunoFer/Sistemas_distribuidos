# coding: utf-8

import socket

while True:
	socketServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	socketServer.bind(('10.3.1.49',8888))
	dados, dadosCliente = socketServer.recvfrom(1024)
	dados = dados.split()
	print dados
	print dadosCliente
	if dados[0]=="sum":
		resultado = int(dados[1])+int(dados[2])
		socketServer.sendto(str(resultado),(dadosCliente[0],8888))
	elif dados[0]=="pro":
		resultado = int(dados[1])*int(dados[2])
		socketServer.sendto(str(resultado),(dadosCliente[0],7777))
	elif dados[0]=="fat":
		x = int(dados[1])
		resultado = lambda x: 1 if x==1 else x*resultado(x-1)
		socketServer.sendto(str(resultado(x)),(dadosCliente[0],6666))
	socketServer.close()

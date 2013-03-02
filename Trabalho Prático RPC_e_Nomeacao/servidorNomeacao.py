# coding: utf-8

import socket
from multiprocessing import Process, Manager
import time
import exceptions
import os
import re
import base64
from Crypto.Cipher import AES

IP_SERVER = '10.3.1.49'
PORTA_SERVIDOR_NOMES = 8888
PORTA_SERVERS = 7777

class ipFuncoes:
    ip = None
    funcoes = None

    def __init__ (self, ip, funcoes):
        self.ip = ip
        self.funcoes = funcoes

def string_size16(frase):
    parar = False
    cont = len(frase)
    while not parar:
        cont+=1
        if cont==16:
            parar=True
        frase+=" "

    return frase

def verifica():
	i = 51

	print 'Verificando IPs on line...'
	
	while i < 53:
		ip = '10.3.1.{0}'.format(i)

		comando = "ping -c1 -w1 " + ip
		r = "".join(os.popen(comando).readlines())

		obj = ipFuncoes(ip,"")
		if not re.search ("100% packet loss", r):
			lista.append(obj)
		i += 1



socketServerDominio = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
socketServerDominio.bind((IP_SERVER,PORTA_SERVIDOR_NOMES))

manager = Manager()
lista = manager.list()
m1 = Process(target=verifica,args=(lista))
m1.start()
time.sleep(2)
listaServidores = []

#criptografando
chave = 'titicadegalinhas'
cifra = AES.new(chave,AES.MODE_ECB)

if len(lista)!=0:
    print
    print "-------------------------------------"
    print 'Máquinas ligadas na rede: '
    for i in lista:
        try:
            # envia aos servidores uma solicitação
            socketServerDominio.settimeout(1)
            socketServerDominio.sendto("ope",(i.ip,PORTA_SERVERS))
            dados, dadosCliente = socketServerDominio.recvfrom(1024)
            obj = ipFuncoes(i.ip, dados)
            print i.ip, PORTA_SERVERS, dados
            listaServidores.append(obj)
        except:
            print i,"Não implementa nenhum recurso!"
else:
    print "Nenhuma máquina ligada na rede!"

while True:
    socketServerDominio.settimeout(None)
    dados, dadosCliente = socketServerDominio.recvfrom(1024)
    dados = dados.strip()
    print "Requisição: ",dados,dadosCliente
    
    #key = RSA.importKey(dados)
    #print key

    achou=False
    for i in listaServidores:
        fun = i.funcoes.split()
        for k in fun:
            if k == dados:
                print "Enviando o IP {0} para a requisicao {1}".format(i.ip,dadosCliente)
                ipResposta = string_size16(i.ip)
                print len(ipResposta)
                resposta = cifra.encrypt(ipResposta)
                socketServerDominio.sendto(resposta,(dadosCliente))
                achou=True



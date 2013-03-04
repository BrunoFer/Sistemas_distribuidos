# coding: utf-8

import socket
from multiprocessing import Process, Manager
import threading
import time
import exceptions
import os
import re
import base64
from Crypto.Cipher import AES

# settings
FAIXA_IPS = '192.168.1.{0}'
INICIO = 101
FIM = 103
IP_SERVER = '192.168.1.102'
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

def procuraServidores(lista,socketServer):
    while 1:
        lista = []
        print
        print "-------------------------------------"
        print 'Máquinas ligadas na rede: '
        i = INICIO
        while i < FIM:
            ip = FAIXA_IPS.format(i)
            try:
                # envia aos servidores uma solicitação
                socketServer.settimeout(2)
                socketServer.sendto("ope",(ip,PORTA_SERVERS))
                dados, dadosCliente = socketServer.recvfrom(1024)
                obj = ipFuncoes(ip, dados)
                print ip, PORTA_SERVERS, dados
                lista.append(obj)
            except:
                print ip,"Não implementa nenhum recurso!"
            i+=1
        time.sleep(20)


socketServerDominio = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
socketServerDominio.bind((IP_SERVER,PORTA_SERVIDOR_NOMES))

manager = Manager()
lista = manager.list()
t1=threading.Thread(target=procuraServidores,args=(lista,socketServerDominio))
t1.start()

#criptografia AES com os clientes
chave = 'titicadegalinhas'
cifra = AES.new(chave,AES.MODE_ECB)

while True:
    socketServerDominio.settimeout(None)
    dados, dadosCliente = socketServerDominio.recvfrom(1024)
    dados = dados.strip()
    print "Requisição: ",dados,dadosCliente

    achou=""
    
    if len(lista)==0:
        print "Nenhuma máquina ligada na rede!"
    else:
        for i in listaServidores:
            fun = i.funcoes.split()
            for k in fun:
                if k == dados:
                    achou=i.ip

    if achou!="":
        print "Enviando o IP {0} para a requisicao {1}".format(i.ip,dadosCliente)
        ipResposta = string_size16(i.ip)
        #print len(ipResposta)
        resposta = cifra.encrypt(ipResposta)
        socketServerDominio.sendto(resposta,(dadosCliente))
    else:
        print "Enviando a mensagem 'Bosta' para o cliente ".format(dadosCliente)
        resposta = string_size16("Bosta")
        #print len(resposta)
        resposta = cifra.encrypt(resposta)
        socketServerDominio.sendto(resposta,(dadosCliente))

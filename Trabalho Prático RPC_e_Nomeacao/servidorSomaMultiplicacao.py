# coding: utf-8

import socket
from multiprocessing import Process, Manager
import threading
import time
import exceptions
from Crypto.PublicKey import RSA
import pickle

IP_SERVIDOR = '10.3.1.51'
PORTA_SERVIDOR = 7777
private = RSA.generate(1024)
public = private.publickey()

def devolverOperacoes(dados,dadosCliente):
    dadosEnviar = "sum pro"
    print "Enviando Operações"
    socketServer.sendto(dadosEnviar, (dadosCliente[0], dadosCliente[1]))

def soma(dados,dadosCliente,chaveCli):
    socketServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    resultado = int(dados[1])+int(dados[2])
    time.sleep(1)
    print "Resultado da soma: ",resultado
    resultado = chaveCli.encrypt(str(resultado),32)
    socketServer.sendto(resultado[0],(dadosCliente[0],dadosCliente[1]))
    socketServer.close()

def produto(dados,dadosCliente,chaveCli):
    socketServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    resultado = int(dados[1])*int(dados[2])
    time.sleep(1)
    print "Resultado da multiplicação: ",resultado
    resultado = chaveCli.encrypt(str(resultado),32)
    socketServer.sendto(resultado[0],(dadosCliente[0],dadosCliente[1]))
    socketServer.close()

def novaOperacao(dados,dadosCliente,chaveCli):
    if dados[0]=="sum":
        t1 = threading.Thread(target=soma,args=(dados,dadosCliente,chaveCli))
        t1.start()
    elif dados[0]=="pro":
        t1 = threading.Thread(target=produto,args=(dados,dadosCliente,chaveCli))
        t1.start()


socketServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
socketServer.bind((IP_SERVIDOR,PORTA_SERVIDOR))

while True:
    chave, dadosCliente = socketServer.recvfrom(2048)
    chave2 = chave.split()

    if chave2[0]=="ope":
        print chave2,dadosCliente
        t1 = threading.Thread(target=devolverOperacoes,args=(chave2,dadosCliente))
        t1.start()
    
    else:
        chaveCli = pickle.loads(chave)
        print chaveCli
        socketServer.sendto(pickle.dumps(public),(dadosCliente[0],dadosCliente[1]))
        dados, dadosCliente = socketServer.recvfrom(2048)
        msgem = private.decrypt(dados)
        msgem = msgem.split()
        t = threading.Thread(target=novaOperacao,args=(msgem,dadosCliente,chaveCli))
        t.start()



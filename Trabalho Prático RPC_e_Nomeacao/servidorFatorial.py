# coding: utf-8

import socket
from multiprocessing import Process, Manager
import threading
import time
import exceptions
from Crypto.PublicKey import RSA
import pickle

IP_SERVIDOR = '10.3.1.52'
PORTA_SERVIDOR = 7777
private = RSA.generate(1024)
public = private.publickey()

def fatorialDividido(lista,a,b):
	resultado = lambda a: b if a==b else a*resultado(a-1)
	lista.append(resultado(a))

def fatorial(dados,dadosCliente,chaveCli):
    manager = Manager()
    lista = manager.list()
    x = int(dados[1])
    m1 = Process(target=fatorialDividido,args=(lista,x,x/2))
    m2 = Process(target=fatorialDividido,args=(lista,x/2-1,1))
    m1.start()
    m2.start()

    m1.join()
    m2.join()

    time.sleep(2)
    socketServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    resultFatorial=1
    for i in lista:
        resultFatorial *= i
    resultFatorial = chaveCli.encrypt(str(resultFatorial),32)
    socketServer.sendto(resultFatorial[0],(dadosCliente[0],dadosCliente[1]))


def devolveOperacoes(dados,dadosCliente):
	dadosEnviar = "fat"
	socketServer.sendto(dadosEnviar,(dadosCliente[0],dadosCliente[1]))


socketServer = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
socketServer.bind((IP_SERVIDOR,PORTA_SERVIDOR))

while True:
    chave, dadosCliente = socketServer.recvfrom(2048)
    chave2 = chave.split()

    if chave2[0]=="ope":
        print chave2,dadosCliente
        t1 = threading.Thread(target=devolveOperacoes,args=(chave2,dadosCliente))
        t1.start()
    else:
        chaveCli = pickle.loads(chave)
        socketServer.sendto(pickle.dumps(public),(dadosCliente[0],dadosCliente[1]))
        dados, dadosCliente = socketServer.recvfrom(2048)
        msgem = private.decrypt(dados)
        msgem = msgem.split()
        t = threading.Thread(target=fatorial,args=(msgem,dadosCliente,chaveCli))
        t.start()



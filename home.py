#!/usr/bin/env python3
import sys
import time
import random
import multiprocessing
import sysv_ipc
import concurrent.futures
import os

key = 666
conso= 50
prod = 100


#utiliser close() et terminate() pour mettre fin à l'utilisation des ressources

def maison(cons,prod,mq):
    #print("dans une maison")
    etat = random.randint(1, 3)
    while True :
        meteo = random.randint(10, 30) #ici on ira chercher la valeur dans la mémoire partagée
        cons = cons + meteo
        if cons<0 :
            cons = 0
        print(os.getpid(),"avec prod =",prod,"et cons=",cons)
        energie = prod - cons
        print("energie =",energie)
        if energie<0:
            message = str(os.getpid())
            mq.send(message, type=3)
            print("énergie demandé")
            don, type = mq.receive(True,2)
            print("énergie reçu=",int(don))
            prod  = prod + int(don)
        else :
            if etat == 1 :
                msg = str(energie) # les message dans MessageQueue sont forcément des objets bytes (des string)
                mq.send(msg, type=2)
                print("énergie envoyé",energie)
                prod  = prod - energie
            elif etat == 2 :
                print("on vend au marché")
            else :
                print("vérifie si mendiant")

        """
        print(os.getpid(),"avec prod =",prod,"et cons=",cons)
        time.sleep(2)


if __name__ == "__main__":
    try:
        #mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
        mq = sysv_ipc.MessageQueue(key)
    except ExistentialError:
        print("Message queue", key, "already exsits, terminating.")
        sys.exit(1)

    processes = []
    for i in range(5):
        process = multiprocessing.Process(target=maison, args=(conso,prod,mq))
        processes.append(process)
        process.start()

    for proc in processes :
        proc.join() #on attend la fin du proc pour le terminer
    mq.remove()

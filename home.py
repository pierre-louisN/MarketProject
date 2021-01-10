#!/usr/bin/env python3
import sys
import time
import random
import multiprocessing
import sysv_ipc
import concurrent.futures
import os
import signal

key = 666
conso= 50
prod = 100

# types : 2 (demande énergie), 3 (don énergie), 4 (vendre au marché)
#remarque il faut utiliser des signaux pour démarrer les jobs
#utiliser close() et terminate() pour mettre fin à l'utilisation des ressources

def maison(cons,prod,mq):
    #print("dans une maison")
    etat = random.randint(1, 3)
    while True :
        meteo = random.randint(-10, 30) #ici on ira chercher la valeur dans la mémoire partagée
        cons = cons - meteo #si temp > 0 alors consommation diminue (l'inverse sinon)
        #prod = prod +10
        if cons<0 :
            cons = 0
        print(os.getpid(),": production =",prod,"et consommation =",cons)
        energie = prod - cons
        print(os.getpid(),": energie =",energie)
        if energie<0:
            message = str(os.getpid())
            mq.send(message, type=3)
            print(os.getpid(),": demande énergie")
            don, type = mq.receive(True,2)
        #    print(os.getpid(),": reception energie =",int(don))
            prod  = prod + int(don)
        else :
            msg = str(energie) # les message dans MessageQueue sont forcément des objets bytes (des string)
            prod  = prod - energie
            if etat == 1 :
                mq.send(msg, type=2)
        #        print(os.getpid(),": a envoyé son énergie",energie)
            elif etat == 2 :
        #        print(os.getpid(),": a vendu au marché")
                mq.send(msg, type=4)
            else :
                print(os.getpid(),": vérifie s'il y a des mendiant")
                try :
                    dem, type = mq.receive(False,3) #on regarde si il y a des demandes mais on ne se bloque pas
                    mq.send(msg, type=2)
                    print(str(dem))
        #            print(os.getpid(),": a donnée à maison mendiante")
                except sysv_ipc.BusyError : #si aucune maison ne demande de l'énergie
                    print(os.getpid(),": Aucun mendiant, vend au marché")
                    mq.send(msg, type=4)

        print(os.getpid(),": prod =",prod,"et cons=",cons)
        time.sleep(2)


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    print('You pressed Ctrl+C!')
    print('fin du processus home')


if __name__ == "__main__":
    try:
        #mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)

        mq = sysv_ipc.MessageQueue(key)
        #mq.clear()
    except ExistentialError:
        print("Message queue", key, "already exsits, terminating.")
        sys.exit(1)

    processes = []
    for i in range(10):
        process = multiprocessing.Process(target=maison, args=(conso,prod,mq))
        processes.append(process)
        process.start()

    for proc in processes :
        proc.join() #on attend la fin du proc pour le terminer

    signal.signal(signal.SIGINT, handler)
    print('> Ctrl+C, fin de home.py ...')

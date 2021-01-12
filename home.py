#!/usr/bin/env python3
import sys, traceback
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
maisons = 10
# types : 2 (demande énergie), 3 (don énergie), 4 (vendre au marché), 5 (achat au marché), 6 (fin de communication)
#remarque il faut utiliser des signaux pour démarrer les jobs
#utiliser close() et terminate() pour mettre fin à l'utilisation des ressources

def maison(cons,prod,mq):
    etat = random.randint(1, 3)
    while True :
        meteo = random.randint(-10, 30) #ici on ira chercher la valeur dans la mémoire partagée
        cons = cons - meteo #si temp > 0 alors consommation diminue (l'inverse sinon)
        if cons<0 :
            cons = 0
        print(os.getpid(),": production =",prod,"et consommation =",cons)
        energie = prod - cons
        print(os.getpid(),": energie =",energie)
        if energie<=0: # manque d'nergie
            message = str(os.getpid())
            mq.send(message, type=3)
            print(os.getpid(),": demande énergie")
            try :
                don, type = mq.receive(False,2) # on regarde s'il y a des donneurs
                print(os.getpid(),": reception energie =",int(don))
                prod  = prod + int(don)
            except sysv_ipc.BusyError : #si aucune maison ne donne de l'énergie
                mq.send(msg, type=5)
                print(os.getpid(),": Aucun donneur, achete l'energie manquante au marché")
                prod = prod + abs(prod-cons)
        else :
            msg = str(energie) # les message dans MessageQueue sont forcément des objets bytes (des string)
            prod  = prod - energie # on met à jour la production
            if etat == 1 : # don du surplus
                mq.send(msg, type=2)
                print(os.getpid(),": a envoyé son énergie",energie)
            elif etat == 2 : # vente du surplus
                mq.send(msg, type=4)
                print(os.getpid(),": a vendu au marché")

            else : # vente du surplus si aucun mendiant
                print(os.getpid(),": vérifie s'il y a des mendiant")
                try :
                    dem, type = mq.receive(False,3) #on regarde si il y a des demandes mais on ne se bloque pas
                    mq.send(msg, type=2)
                    print(os.getpid(),": a donnée",energie,"à maison mendiante")
                except sysv_ipc.BusyError : #si aucune maison ne demande de l'énergie
                    mq.send(msg, type=4)
                    print(os.getpid(),": Aucun mendiant, vend au marché")

        print(os.getpid(),": prod =",prod,"et cons=",cons)
        time.sleep(2)
        #pas utiliser time.sleep mais mettre un 'tick' dans market pour synchro ou utiliser une barrière avec multiprocessing.Barrier


if __name__ == "__main__":
    try:
        #mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
        mq = sysv_ipc.MessageQueue(key)
        #mq.clear()

    except sysv_ipc.ExistentialError:
        print("Message queue", key, "doesnt exists, terminating.")
        sys.exit(1)

    processes = []

    for i in range(maisons): #initialise les maisons
        process = multiprocessing.Process(target=maison, args=(conso,prod,mq))
        processes.append(process)
        process.start()

    try :
        for proc in processes :
            proc.join() #on attend la fin du proc pour le terminer

    except KeyboardInterrupt :
        print("\n"+'Ctrl+C')
        print('Fin du processus home')

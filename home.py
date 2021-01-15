#!/usr/bin/env python3
from multiprocessing import shared_memory, Process
import sys, traceback
import time
import random
import sysv_ipc
import concurrent.futures
import os
import signal

# types : 2 (demande énergie), 3 (don énergie), 4 (vendre au marché), 5 (achat au marché), 6 (fin de communication)
#remarque il faut utiliser des signaux pour démarrer les jobs
#utiliser close() et terminate() pour mettre fin à l'utilisation des ressources

class maison :

    key = 666 
    consommation= 50 # la prod et la cons vont suivre une loi normale centrée autour d'une valeur 
    production = 100
    maisons = 10

    def __init__(self, barrier, temp):
        print("Debut home")
        try:
            mq = sysv_ipc.MessageQueue(self.key)

        except sysv_ipc.ExistentialError:
            print("Message queue", self.key, "doesnt exists")
            sys.exit(1)
        
        etat = random.randint(1, 3)
        cons = self.consommation
        prod = self.production
        temps = 0
        while True :
            with temp.get_lock():
                meteo = temp.value
            cons = cons - meteo #si temp > 0 alors consommation diminue (l'inverse sinon)
            if cons<0 :
                cons = 0
            #print(os.getpid(),": production =",prod,"et consommation =",cons)
            energie = prod - cons
            #print(os.getpid(),": energie =",energie)
            if energie<=0: # manque d'energie
                message = str(os.getpid())
                mq.send(message, type=3)
                #print(os.getpid(),": demande énergie")
                try :
                    don, type = mq.receive(False,2) # on regarde s'il y a des donneurs
                    #print(os.getpid(),": reception energie =",int(don))
                    prod  = prod + int(don)
                except sysv_ipc.BusyError : #si aucune maison ne donne de l'énergie
                    mq.send(msg, type=5)
                    #print(os.getpid(),": Aucun donneur, achete l'energie manquante au marché")
                    prod = prod + abs(prod-cons)
            else :
                msg = str(energie) # les message dans MessageQueue sont forcément des objets bytes (des string)
                prod  = prod - energie # on met à jour la production
                if etat == 1 : # don du surplus
                    mq.send(msg, type=2)
                    #print(os.getpid(),": a envoyé son énergie",energie)
                elif etat == 2 : # vente du surplus
                    mq.send(msg, type=4)
                    #mq.send(msg, block = False, type=4)
                    #print(os.getpid(),": a vendu au marché")

                else : # vente du surplus si aucun mendiant
                    #print(os.getpid(),": vérifie s'il y a des mendiant")
                    try :
                        dem, type = mq.receive(False,3) #on regarde si il y a des demandes mais on ne se bloque pas
                        mq.send(msg, type=2)
                        #print(os.getpid(),": a donnée",energie,"à maison mendiante")
                    except sysv_ipc.BusyError : #si aucune maison ne demande de l'énergie
                        mq.send(msg, type=4)
                        #print(os.getpid(),": Aucun mendiant, vend au marché")
            if temps % 3600 == 0:
                print("Jour n°",temps // 3600,os.getpid(),": prod =",prod,"et cons=",cons)
            temps += 1
            barrier.wait()
        mem.shm.close()
        mem.shm.unlink()
        mq.remove()
        print("Fin Home")




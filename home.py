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
        secondes = 0
        while True :
            try : 
                with temp.get_lock():
                    meteo = temp[0]
                    cat = 0
                    catastrophe = temp[1]
                    if catastrophe == 9 :
                        tempête_de_neige= True
                        cat = - 0.25
                    if catastrophe == 3 :
                        inondation = True
                        cat = - 0.1
                    if catastrophe == 0 : 
                        ouragan = True
                        cat = - 0.3
                    if catastrophe == 0 : 
                        tornade = True
                        cat = - 0.1
                cons = cons - meteo #si temp > 0 alors consommation diminue (l'inverse sinon), en vrai c'est bizarre ta conso augmente 
                cons = cons + ( cat * cons )  #une catastrophe crée des coupures de courant etc, les services sont coupés donc moins de conso  
                if cons<0 :                                                                #seulement à partir de -1 degré, c'est un peu bas
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
            except KeyboardInterrupt :
                print("Ctrl +c attrapé dans home")
                break
            except sysv_ipc.Error :
                print("Error")
                break
            """
            if secondes % 3600 == 0:
                print("Jour n°",secondes // 3600,os.getpid(),": prod =",prod,"et cons=",cons)
            """
            print("Jour n°",secondes,os.getpid(),": prod =",prod,"et cons=",cons)
            secondes += 1
            barrier.wait()
        
        mq.remove()
        print("Fin Home")




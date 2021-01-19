#!/usr/bin/env python3
import threading
import sys, traceback
import time
import random
import sysv_ipc
import os
import signal
import numpy
# types : 2 (demande énergie), 3 (don énergie), 4 (vendre au marché), 5 (achat au marché), 6 (fin de communication)
#remarque il faut utiliser des signaux pour démarrer les jobs
#utiliser close() et terminate() pour mettre fin à l'utilisation des ressources
# pip3 install numpy pour installer numpy et utiliser la loi normale

class maison :

    key = 666 
    consommation= 50 # la prod et la cons vont suivre une loi normale centrée autour d'une valeur 
    production = 100
    # numpy.random.normal(loc=0.0, scale=1.0, size=None)¶ loc = le centre de la distribution; scale : deviation standard de la distribution 
    maisons = 10
    fin = False

    def envoi(self,mq,msg,type) :
        try :
            mq.send(msg,type=type)
        except sysv_ipc.ExistentialError :
            #print("Queue supprimé")
            self.fin = True


    def __init__(self, barrier, temp, nom):
        print("Debut",nom) # les maisons sont numérotés pour pouvoir débug plus facilement
        try:
            mq = sysv_ipc.MessageQueue(self.key)

        except sysv_ipc.ExistentialError:
            print("Message queue", self.key, "doesnt exists")
            sys.exit(1)
        
        etat = random.randint(1, 3)
        #cons = self.consommation
        #prod = self.production
        cons = numpy.random.normal(loc=50.0, scale=10.0, size=None)
        prod = numpy.random.normal(loc=100.0, scale=10.0, size=None)
        print(nom,"conso =",cons,"et prod",prod)
        secondes = 0
        while not(self.fin) :
            try : 
                with temp.get_lock():
                    meteo = temp[0]
                    cat = 0
                    catastrophe = temp[1]
                    if catastrophe == 2 :
                        tempête_de_neige= True
                        print("TEMPÊTE")
                        cat =  0.25
                    if catastrophe == 4 :
                        inondation = True
                        print("INONDATION")
                        cat = 0.1
                    if catastrophe == 6 : 
                        ouragan = True
                        print("OURAGAN")
                        cat = 0.3
                    if catastrophe == 8 : 
                        tornade = True
                        print("TORNADE")
                        cat = 0.1
                cons = cons - meteo #si temp > 0 alors consommation diminue (l'inverse sinon), en vrai c'est bizarre ta conso augmente, la conso augmente quand il fait froid (chauffage, etc ...)
                cons = cons + ( cat * cons )  #une catastrophe crée des coupures de courant etc, les services sont coupés donc moins de conso, #seulement à partir de -1 degré, c'est un peu bas
                #if cons<0 : # la consommation,  la conso ne  peut pas être négatif dans la réalité                                                          
                #    cons = 0
                #print(os.getpid(),": production =",prod,"et consommation =",cons)
                energie = prod - cons
                print(nom,": energie =",energie)
                if energie<=0: # manque d'energie
                    message = str(os.getpid())
                    #mq.send(message, type=3)
                    self.envoi(mq,message,3)
                    print(nom,": demande énergie")
                    try :
                        don, type = mq.receive(False,2) # on regarde s'il y a des donneurs
                        print(nom,": reception energie =",float(don))
                        prod  = prod + float(don)
                    except sysv_ipc.BusyError : #si aucune maison ne donne de l'énergie
                        #mq.send(msg, type=5)
                        self.envoi(mq,msg,5)
                        print(nom,": Aucun donneur, achete l'energie manquante au marché")
                        prod = prod + abs(prod-cons)
                else :
                    msg = str(energie) # les message dans MessageQueue sont forcément des objets bytes (des string)
                    prod  = prod - energie # on met à jour la production
                    if etat == 1 : # don du surplus
                        #mq.send(msg, type=2)
                        self.envoi(mq,msg,2)
                        print(nom,": a envoyé son énergie",energie)
                    elif etat == 2 : # vente du surplus
                        #mq.send(msg, type=4)
                        self.envoi(mq,msg,4)
                        #mq.send(msg, block = False, type=4)
                        print(nom,": a vendu au marché")

                    else : # vente du surplus si aucun mendiant
                        #print(os.getpid(),": vérifie s'il y a des mendiant")
                        try :
                            dem, type = mq.receive(False,3) #on regarde si il y a des demandes mais on ne se bloque pas
                            #mq.send(msg, type=2)
                            self.envoi(mq,msg,2)
                            print(nom,": a donnée",energie,"à maison mendiante")
                        except sysv_ipc.BusyError : #si aucune maison ne demande de l'énergie
                            #mq.send(msg, type=4)
                            self.envoi(mq,msg,4)
                            print(nom,": Aucun mendiant, vend au marché")

            except sysv_ipc.Error :
                #print("Error")
                self.fin = True
            
            if secondes == 60 :
                self.fin = True
            #print("Jour n°",secondes,os.getpid(),": prod =",prod,"et cons=",cons)
            secondes += 1
            try :
                barrier.wait()
            except threading.BrokenBarrierError: 
                #print("barriere supprimé")
                self.fin = True
        try :
            mq.remove()
        except sysv_ipc.ExistentialError:
            pass
            #print("Queue supprimé, fin de",nom)

        try :
            barrier.reset()
        except threading.BrokenBarrierError :
            #print("barriere supprimé")
            self.fin = True       
        #print("Fin",nom)




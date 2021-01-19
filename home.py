#!/usr/bin/env python3
import threading
import sys, traceback
import time
import random
import sysv_ipc
import os
import signal
import numpy

# types : 2 (demande énergie), 3 (don énergie), 4 (vendre au marché), 5 (achat au marché), 6 (envoi du prix actuel)
# pip3 install numpy pour installer numpy et utiliser la loi normale
# (1 tour dans la boucle = 1 jour), dure 365 jours maximum

class maison :

    key = 666
    fin = False
    
    def envoi(self,mq,m,type) : #envoi un message dans la MessageQueue
        try :
            mq.send(m,type=type)
        except sysv_ipc.ExistentialError :
            self.fin = True
        
        except KeyboardInterrupt :
                self.fin = True


    def __init__(self, barrier, temp, nom):
        try:
            mq = sysv_ipc.MessageQueue(self.key)

        except sysv_ipc.ExistentialError:
            print("Message queue", self.key, "doesnt exists")
            sys.exit(1)
        
        etat = random.randint(1, 3)
        
        jours = 0
        while not(self.fin) :
            cons = numpy.random.normal(loc=47.0, scale=5.0, size=None)
            prod = numpy.random.normal(loc=45.0, scale=5.0, size=None)
            #print(nom,"conso =",cons,"et prod",prod)
            try : 
                with temp.get_lock():
                    meteo = temp[0]
                    coeff = 0
                    evenement = temp[1]
                    if evenement == 25 :
                        print("\nTEMPÊTE DE NEIGE\n") # les gens sont bloqués chez eux et ils mettent le chauffage donc la consommation augmente
                        coeff =  0.5 
                    if evenement == 75 :
                        print("\nCANICULE\n") # il fait très chaud, activation de la climatisation donc la consommation augmente
                        coeff =  0.3

                cons = cons - meteo #si temp > 0 alors consommation diminue (l'inverse sinon), en vrai c'est bizarre ta conso augmente, la conso augmente quand il fait froid (chauffage, etc ...)
                cons = cons + ( coeff * cons )  #une catastrophe crée des coupures de courant etc, les services sont coupés donc moins de conso, #seulement à partir de -1 degré, c'est un peu bas
                energie = prod - cons
                #print(nom,": energie =",energie)
                msg = str(abs(energie)) # on ne peut envoyer que des Bytes (str) dans la MessageQueue
                if energie<=0: # manque d'energie
                    self.envoi(mq,msg,3)
                    print(nom,": demande",msg)
                    try :
                        don, type = mq.receive(False,2) # on regarde s'il y a des donneurs
                        print(nom,": reception de",float(don))
                    except sysv_ipc.BusyError : #si aucune maison ne donne de l'énergie
                        self.envoi(mq,msg,5)
                        try :
                            prix, type = mq.receive(False,type = 6)
                            print(nom,": aucun donneur, achete ",msg,"au marché ( prix =",str(prix.decode()),")")
                        except sysv_ipc.BusyError :
                            pass
                else : # surplus d'energie
                    if etat == 1 : # don du surplus
                        self.envoi(mq,msg,2)
                        print(nom,": a donné",msg)
                    elif etat == 2 : # vente du surplus
                        self.envoi(mq,msg,4)
                        print(nom,": a vendu",msg," au marché")
                    else : # vente du surplus si aucun mendiant
                        try :
                            dem, type = mq.receive(False,3) #on regarde si il y a des demandes mais on ne se bloque pas
                            self.envoi(mq,msg,2)
                            print(nom,": a donnée",msg,"à maison mendiante")
                        except sysv_ipc.BusyError : #si aucune maison ne demande de l'énergie
                            self.envoi(mq,msg,4)
                            print(nom,": aucun mendiant, vend",msg,"au marché")

            except sysv_ipc.Error :
                self.fin = True
            
            except KeyboardInterrupt :
                self.fin = True
            
            if jours == 365 : # la simulation dure 1 an maximum 
                self.fin = True

            jours += 1
            try :
                barrier.wait() #se synchronise avec les autres processus
            except threading.BrokenBarrierError: 
                self.fin = True
            except KeyboardInterrupt :
                self.fin = True
        try : 
            mq.remove()
        except sysv_ipc.ExistentialError:
            pass

        try :
            barrier.reset() #on indique aux autres processus que la simulation est fini
        except threading.BrokenBarrierError : #si la barriere a déjà eté supprimé alors fin
            self.fin = True  




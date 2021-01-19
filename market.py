#!/usr/bin/env python3
import sys
import time
import sysv_ipc
import concurrent.futures
import signal
import os
from multiprocessing import Process, Barrier
from random import *
import threading


class market:

    key = 666
    crise = False
    guerre = False
    fin = False
    jours = 0

    def worker(self, cout, m, t): #gére  les transactions avec les maisons
        if t == 4 : # vente
            #print(float(m.decode()),"vendu")
            cout  = cout - (float(m) * 0.01) # plus d'énergie disponible donc le prix baisse
        elif t == 5 : # achat
            #print(float(m.decode()),"acheté")
            cout = cout + (float(m) * 0.01) # moins d'énergie disponible donc le prix augmente
        else :
            pass
        return cout


    def economics(self,barrier): #fils de market, indique si il y a une crise ou pas
        #une chance sur 30 qu'il y ait une crise
        print("Début Economics")
        while not(self.fin):
            test = randint(0,30) 
            if test == 15 :
                if (self.crise):
                    print("\n FIN CRISE\n")
                    self.crise = False
                else :
                    print("\nCRISE\n")
                    self.crise = True
                os.kill(int(os.getppid()), signal.SIGUSR1) #previent le père que 'crise' a changé

            self.wait(barrier)
        print("Fin Economics")

    
    def politics(self,barrier): #fils de market, indique si il y a une guerre ou pas
        #une chance sur 50 qu'il y ait une guerre
        print("Début Politics")
        while not(self.fin):
            test = randint(0,50) 
            if test == 25 :
                if (self.guerre):
                    print("\n FIN GUERRE\n")
                    self.guerre = False
                else :
                    print("\nGUERRE\n")
                    self.guerre = True
                os.kill(int(os.getppid()), signal.SIGUSR2) #previent le père que 'guerre' a changé
            self.wait(barrier)
        print("Fin Politics")

        
    def handler(self, sig, frame): #gere les signaux
        if sig == signal.SIGUSR1:
            self.crise = not (self.crise) 
        if sig == signal.SIGUSR2:
            self.guerre = not (self.guerre)
        if sig == signal.SIGINT:
            self.fin = True
    

    def wait(self, barrier): #attendre et quitter si la barrier a été reset
        try :
            barrier.wait()
        except threading.BrokenBarrierError :
            self.fin = True

    def __init__(self, barrier):
        
        print("Début Market")
        try:
            mq = sysv_ipc.MessageQueue(self.key) # on se connecte à la queue

        except sysv_ipc.ExistentialError:
            print("Message queue", self.key, "doesnt exists")
            sys.exit(1)

        #handler permet de changer les etats des evenements en fonctions du signal reçu
        signal.signal(signal.SIGUSR1, self.handler)
        signal.signal(signal.SIGUSR2, self.handler)
        signal.signal(signal.SIGINT, self.handler)   

        #processus fils
        politics = Process(target=self.politics, args=(barrier,))
        economics = Process(target=self.economics, args=(barrier,))

        politics.start()
        economics.start()

        with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor: #limite  de 10 pour gérer les transactions avec les maisons
            cout = 5 # cout de l'energie
            while not(self.fin):

                try :
                    m, t = mq.receive(False)
                    if t == 5 : # on envoie le prix si un achat a été fait
                        try :
                            mq.send(str(cout),type=6) # on envoi le prix pour que les maisons qui achétent l'affichent
                        except sysv_ipc.ExistentialError :
                            self.fin = True

                    calc = executor.submit(self.worker, cout, m ,t)
                    cout = calc.result()

                    if (self.guerre) :
                        cout  = cout + cout *0.2
                    if (self.crise) :
                        cout  = cout + cout *0.1

                    if cout<0: # le cout ne peut pas être négatif 
                        cout = 0
                    print("\n","Jour n°",self.jours,"prix de l'energie est",cout,"\n")
                
                except sysv_ipc.Error :
                    self.fin = True
                
                except KeyboardInterrupt :
                    self.fin = True

                self.jours += 1
                self.wait(barrier)
        
        politics.join()
        economics.join()
        try :
            mq.remove()
        except sysv_ipc.ExistentialError:
            pass
        print("Fin Market")



    



    

    




    




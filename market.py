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

    def worker(self, cout, m, t): #gére  les transactions avec les maisons
        if t == 4 : # vente
            #print("Maison veut vendre",int(m),"d'energie")
            cout  = cout - (float(m) * 0.01) # plus d'énergie disponible donc le prix baisse
        elif t == 5 : # achat
            #print("Maison veut acheter",int(m),"d'energie")
            cout = cout + (float(m) * 0.01) # moins d'énergie disponible donc le prix augmente
        else :
            #print("Aucune transaction")
            pass
        return cout


    def economics(self,barrier):
        #tous les 30 secondes on va générer un évènements aléatoires
        print("Début Economics")
        secondes = 0
        while not(self.fin):
            test = randint(0,100)
            if test == 50 :
                print("CRISE est modifié")
                os.kill(int(os.getppid()), signal.SIGUSR1)  #guerre = True
            self.wait(barrier)
        print("Fin Economics")


    
    def politics(self,barrier):
        print("Début Politics")
        secondes = 0
        while not(self.fin):
            test = randint(0,100) #un evenement à une chance sur 100 d'arriver
            if test == 50 :
                print("GUERRE est modifié")
                os.kill(int(os.getppid()), signal.SIGUSR2)  #guerre = True
            self.wait(barrier)
            #time.sleep(2)
        print("Fin Politics")
                

        
    def handler(self, sig, frame):
        if sig == signal.SIGUSR1:
            self.crise = not (self.crise)
        if sig == signal.SIGUSR2:
            self.guerre = not (self.guerre)
        if sig == signal.SIGINT:
            self.fin = True
    
    def wait(self, barrier):
        try :
            barrier.wait()
        except threading.BrokenBarrierError :
            #print("barriere supprimé")
            self.fin = True

    def __init__(self, barrier):
        
        print("Début Market")
        try:
            mq = sysv_ipc.MessageQueue(self.key)

        except sysv_ipc.ExistentialError:
            print("Message queue", self.key, "doesnt exists")
            sys.exit(1)

        signal.signal(signal.SIGUSR1, self.handler)
        signal.signal(signal.SIGUSR2, self.handler)
        signal.signal(signal.SIGINT, self.handler)   

        politics = Process(target=self.politics, args=(barrier,))
        economics = Process(target=self.economics, args=(barrier,))

        politics.start()
        economics.start()

        with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor: #limite  de 10 pour gérer les transactions avec les maisons
            cout = 5 # cout de l'energie
            secondes = 0
            while not(self.fin):
                
                try :
                    
                    m, t = mq.receive(False)
                    calc = executor.submit(self.worker, cout, m ,t)
                    cout = calc.result()
                    if (self.guerre) :
                        cout  = cout + cout *0.5 
                    if (self.crise) :
                        cout  = cout + cout *0.2
                    print("Jour n°",secondes,"prix de l'energie est",cout)
                
                except sysv_ipc.Error :
                    #print("error ")
                    self.fin = True

                secondes += 1
                self.wait(barrier)
            
        
        
        politics.join()
        economics.join()
        try :
            mq.remove()
        except sysv_ipc.ExistentialError:
            pass
            #print("Queue supprimé")
        print("Fin Market.")



    



    

    




    




#!/usr/bin/env python3
import sys
import time
import sysv_ipc
import concurrent.futures
import signal
import os
from multiprocessing import Process
from random import *


class market:

    key = 666
    crise = False
    guerre = False
    fin = False

    def worker(self, cout, m, t): #gére  les transactions avec les maisons
            if t == 4 : # vente
                #print("Maison veut vendre",int(m),"d'energie")
                cout  = cout - (int(m) * 0.01) # plus d'énergie disponible donc le prix baisse
            elif t == 5 : # achat
                #print("Maison veut acheter",int(m),"d'energie")
                #print("Marché fait la transaction") # es ce que c'est nécessaire d'envoyer quelque chose dans la queue ici ?
                cout = cout + (int(m) * 0.01) # moins d'énergie disponible donc le prix augmente
            else :
                #print("Aucune transaction")
                pass
            return cout

    def economics(self,barrier):
        #tous les 30 secondes on va générer un évènements aléatoires
        print("Début Economics")
        secondes = 0
        while not(self.fin):
            if secondes % 3600 == 0:
                test = randint(0,1)
                if test == 1 :
                    #print("crise")
                    os.kill(os.getppid(), signal.SIGUSR1)  #guerre = True
                if test ==0 :
                    #print("pas crise")
                    os.kill(os.getppid(), signal.SIGUSR1)  #guerre = True
            barrier.wait()
            #time.sleep(2)


    
    def politics(self,barrier):
        print("Début Politics")
        secondes = 0
        while not(self.fin):
            if secondes % 3600 == 0:
                test = randint(0,1)
                if test == 1 :
                    #print("guerre")
                    os.kill(os.getppid(), signal.SIGUSR2)  #guerre = True
                if test == 0 :
                    #print("pas guerre")
                    os.kill(os.getppid(), signal.SIGUSR2)  #guerre = True
            barrier.wait()
            #time.sleep(2)
                

        
    def handler(sig, frame):
        if sig == signal.SIGUSR1:
            crise = True
        if sig == signal.SIGUSR2:
            guerre = True
        if sig == signal.SIGINT:
            self.fin = True


    def __init__(self, barrier):
        print("Début Market")
        try:
            mq = sysv_ipc.MessageQueue(self.key)

        except sysv_ipc.ExistentialError:
            print("Message queue", self.key, "doesnt exists")
            sys.exit(1)

        pere = os.getpid()
        politics = Process(target=self.politics, args=(barrier,))
        economics = Process(target=self.economics, args=(barrier,))

        signal.signal(signal.SIGUSR1, self.handler)

        politics.start()
        economics.start()

        with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor: #limite  de 10 pour gérer les transactions avec les maisons
            couts = [5] # cout de l'energie
            secondes = 0
            print(self.fin)
            while not(self.fin):
                # on va regarder les signaux pour economics et politics
                try : 
                    m, t = mq.receive(False)
                    #calc = executor.submit(self.worker(m, t, cout)).
                    futures = [executor.submit(self.worker, cout, m, t) for cout in couts]
                    for future in concurrent.futures.as_completed(futures):
                        if guerre and crise :
                            couts = [future.result()+0,5*couts[0]]
                        if guerre or crise :
                            couts = [future.result()+0,5*couts[0]]
                        else :
                            couts = [future.result()]
                        
                    #cout[0] = calc.result()
                except sysv_ipc.BusyError : 
                    pass
                    #print("Aucune transaction")
                
                except KeyboardInterrupt :
                    print("Crtl + C")
                    self.fin = True
                
                if secondes % 3600 == 0:
                    print("Jour n°",temps // 3600,"prix de l'energie est",couts[0])
                
                secondes += 1
                #print("prix actuelle de l'energie est",cout)
                #print(barrier.n_waiting,"procs qui attendent")
                barrier.wait()
                
            print("Fin Market.")
            politics.join()
            economics.join()
            mq.remove()


    



    

    




    




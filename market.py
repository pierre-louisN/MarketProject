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
            test = randint(0,1)
            if test == 1 :
                print("crise")
                os.kill(int(os.getppid()), signal.SIGUSR1)  #guerre = True
            if test ==0 :
                print('pas crise')
                os.kill(int(os.getppid()), signal.SIGUSR1)  #guerre = True
            barrier.wait()


    
    def politics(self,barrier):
        print("Début Politics")
        secondes = 0
        while not(self.fin):
            test = randint(0,1)
            if test == 1 :
                print("guerre")
                os.kill(int(os.getppid()), signal.SIGUSR2)  #guerre = True
            if test == 0 :
                print("pas guerre")
                os.kill(int(os.getppid()), signal.SIGUSR2)  #guerre = True
            barrier.wait()
            #time.sleep(2)
        print("Fin politics")
                

        
    def handler(sig, frame):
        if sig == signal.SIGUSR1:
            crise = True
        if sig == signal.SIGUSR2:
            guerre = True
        if sig == signal.SIGINT:
            self.fin = True

    def test(self):
        while True:
            time.sleep(1)
            print('dans le fils')

    def __init__(self, barrier):
        print("Début Market")
        try:
            mq = sysv_ipc.MessageQueue(self.key)

        except sysv_ipc.ExistentialError:
            print("Message queue", self.key, "doesnt exists")
            sys.exit(1)

        """
        test = Process(target=self.test)
        test.start()
        while True :
            time.sleep(1)
            print('dans le père')
        """    
        politics = Process(target=self.politics, args=(barrier,))
        economics = Process(target=self.economics, args=(barrier,))

        politics.start()
        economics.start()

        with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor: #limite  de 10 pour gérer les transactions avec les maisons
            couts = 5 # cout de l'energie
            secondes = 0
            while not(self.fin):
                # on va regarder les signaux pour economics et politics
                try : 
                    m, t = mq.receive(False)
                    calc = executor.submit(self.worker(m, t, cout))
                    print("energie =",calc.result())
                    """
                    futures = [executor.submit(self.worker, cout, m, t) for cout in couts]
                    for future in concurrent.futures.as_completed(futures):
                        if guerre and crise :
                            couts = [future.result()+0,5*couts[0]]
                        if guerre or crise :
                            couts = [future.result()+0,5*couts[0]]
                        else :
                            couts = [future.result()]
                    """
                    #print("Jour n°",temps,"prix de l'energie est",couts[0])
                        
                    #cout[0] = calc.result()
                except sysv_ipc.BusyError : 
                    pass
                    #print("Aucune transaction")
                
                except KeyboardInterrupt :
                    print("Crtl + C attrapé dans market")
                    self.fin = True
                
                except sysv_ipc.Error :
                    print("error ")
                    break
                """"
                if secondes % 60 == 0:
                    print("Jour n°",temps // 3600,"prix de l'energie est",couts[0])
                if secondes == 10800:
                    break
                """
                secondes += 1
                #print("prix actuelle de l'energie est",cout)
                #print(barrier.n_waiting,"procs qui attendent")
                barrier.wait()
            
            signal.signal(signal.SIGUSR1, self.handler)
            print("Fin Market.")
            politics.join()
            economics.join()
            mq.remove()


    



    

    




    




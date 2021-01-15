#!/usr/bin/env python3
import sys
import time
import sysv_ipc
import concurrent.futures
import signal
import os

class market:

    key = 666

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

    def __init__(self, barrier):
        print("Demarrage Market")
        try:
            mq = sysv_ipc.MessageQueue(self.key, sysv_ipc.IPC_CREX)

        except sysv_ipc.ExistentialError:
            #print("Message queue", self.key, "already exists, connecting in market.")
            mq = sysv_ipc.MessageQueue(self.key)
            mq.remove()
            mq = sysv_ipc.MessageQueue(self.key, sysv_ipc.IPC_CREX)



        with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor: #limite  de 10 pour gérer les transactions avec les maisons
            couts = [5] # cout de l'energie
            temps = 1
            while True:
                # on va regarder les signaux pour economics et politics
                try : 
                    m, t = mq.receive(False)
                    #calc = executor.submit(self.worker(m, t, cout)).
                    futures = [executor.submit(self.worker, cout, m, t) for cout in couts]
                    for future in concurrent.futures.as_completed(futures):
                        couts = [future.result()]
                        
                    #cout[0] = calc.result()
                except sysv_ipc.BusyError : 
                    pass
                    #print("Aucune transaction")
                if temps % 3600 == 0:
                    print("Jour n°",temps // 3600,"prix de l'energie est",couts[0])
                
                temps += 1
                #print("prix actuelle de l'energie est",cout)
                #print(barrier.n_waiting,"procs qui attendent")
                barrier.wait()
                
            print("Fin Market.")
            mq.remove()


    



    

    




    




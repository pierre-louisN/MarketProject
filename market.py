#!/usr/bin/env python3
import sys
import time
import sysv_ipc
import concurrent.futures
import signal
import os

class market:

    key = 666

    def worker(self, m, t, cout): #gére  les transactions avec les maisons
            if t == 4 : # vente
                print("Maison veut vendre",int(m),"d'energie")
                cout  = cout - (int(m) * 0.01) # plus d'énergie disponible donc le prix baisse
            elif t == 5 : # achat
                print("Maison veut acheter",int(m),"d'energie")
                print("Marché fait la transaction") # es ce que c'est nécessaire d'envoyer quelque chose dans la queue ici ?
                cout = cout + (int(m) * 0.01) # moins d'énergie disponible donc le prix augmente
            else :
                cout = 5
            return cout

    def __init__(self, barrier, memory):
        print("Demarrage Market")
        try:
            mq = sysv_ipc.MessageQueue(self.key, sysv_ipc.IPC_CREX)

        except sysv_ipc.ExistentialError:
            #print("Message queue", self.key, "already exists, connecting in market.")
            mq = sysv_ipc.MessageQueue(self.key)

        with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor: #limite  de 10 pour gérer les transactions avec les maisons
            cout = 5 # cout de l'energie
            while True:
                # on va regarder les signaux pour economics et politics
                try : 
                    m, t = mq.receive(False)
                    calc = executor.submit(self.worker(m, t, cout))
                    print(calc.result)
                except sysv_ipc.BusyError : 
                    print("Aucune transaction")

                print("prix actuelle de l'energie est",cout)
                barrier.wait()
                
            print("Fin Market.")
            mq.remove()


    



    

    




    




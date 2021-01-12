#!/usr/bin/env python3
import sys
import time
import sysv_ipc
import concurrent.futures
import signal
import os


key = 666
fin = False

def worker(mq, m, t, cout): #gére  les transactions avec les maisons
    try :
        if t == 4 : # vente
            print("Maison veut vendre",int(m),"d'energie")
            cout  = cout - (int(m) * 0.01) # plus d'énergie disponible donc le prix baisse
        if t == 5 : # achat
            print("Maison veut acheter",int(m),"d'energie")
            print("Marché fait la transaction") # es ce que c'est nécessaire d'envoyer quelque chose dans la queue ici ?
            cout = cout + (int(m) * 0.01) # moins d'énergie disponible donc le prix augmente
        return cout

    except sysv_ipc.SignalError :
        print("controle C")

def signal_handler(sig, frame):
    fin = True
    

if __name__ == "__main__":
    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)

    except sysv_ipc.ExistentialError:
        print("Message queue", key, "already exists, connecting.")
        mq = sysv_ipc.MessageQueue(key)

    print("Demarrage MessageQueue.")


    with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor: #limite  de 10 pour gérer les transactions avec les maisons
        cout = 5 # cout de l'energie
        while True:
                try :
                    m, t = mq.receive(True)
                    calc = executor.submit(worker, mq, m, t, cout)
                    cout = calc.result()
                    print("prix actuelle de l'energie est",cout)
                    #if cout > 10 :
                    #    print("Crise économique") # on va signaler economics

                    signal.signal(signal.SIGINT, signal_handler)
                
                except sysv_ipc.Error:
                    print("\n"+'Fin transactions')
                    # il faut envoyer un signal au maisons pour leur dire de se terminer 
                    break
    
        print("Fin Market.")
        mq.remove()


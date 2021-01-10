#!/usr/bin/env python3
import sys
import time
import sysv_ipc
import concurrent.futures

key = 666


def worker(mq, m, t, cout): #gére  les transactions avec les maisons
    if t == 4 : # vente
        print("Maison veut vendre",int(m),"d'energie")
        cout  = cout * (int(m) * 0.5) # plus d'énergie disponible donc le prix baisse
    if t == 5 : # achat
        print("Maison veut acheter",int(m),"d'energie")
        print("Marché envoie",int(m), "d'énergie")
        mq.send(cout,type = 6)
        cout = cout * (int(m) * 1.2) # moins d'énergie disponible donc le prix augmente
    print("prix de l'energie est",cout)



if __name__ == "__main__":

    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)

    except sysv_ipc.ExistentialError:
        print("Message queue", key, "already exsits, terminating.")
        mq = sysv_ipc.MessageQueue(key)

    print("Demarrage MessageQueue.")

    with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor: #limite  de 10 pour gérer les transactions avec les maisons
        while True:
            cout = 10
            m, t = mq.receive(True)
            print("le type du message est ",t)
            executor.submit(worker, mq, m, t, cout)
            if t == 7 :
                mq.remove()
                ('Fin du processus home')

        mq.remove()


    print("Fin MessageQueue.")

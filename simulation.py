#!/usr/bin/env python3 
import home
import market
from multiprocessing import Barrier, Process, shared_memory, Process
import sysv_ipc

fin = False

def handler(signum, frame):
    fin = True

if __name__== "__main__":

    key = 666

    print("Début simulation")
    b = Barrier(4, timeout=10)
    shm = shared_memory.SharedMemory(create=True, size=10)

    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

    except sysv_ipc.ExistentialError:
        print("Message queue", key, "already exists, connecting.")
        mq = sysv_ipc.MessageQueue(key)

    print("Demarrage MessageQueue.")
    # démarre la barrière 
    #
    marche = Process(target=market.market, args=(b,shm))
    marche.start()
    
    maisons = []

    for i in range(2): #initialise les maisons
        maison = Process(target=home.maison, args=(b,shm))
        maisons.append(maison)
        maison.start()

    while True:
        b.wait()
        if (fin):
            mq.remove
            break
    
    signal.signal(signal.SIGINT, handler)

    
    for proc in maisons :
           proc.join() #on attend la fin du proc pour le terminer
    
    shm.close()
    shm.unlink()
    mq.remove()
    print("Fin simulation")




# ici on va créer les objets et les gérer
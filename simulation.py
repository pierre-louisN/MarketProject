#!/usr/bin/env python3 
import home
import market
import weather
from multiprocessing import Barrier, Process, shared_memory, Process, Lock, Value
import sysv_ipc

fin = False

def handler(signum, frame):
    fin = True

if __name__== "__main__":

    key = 666

    print("Début simulation")
    b = Barrier(4, timeout=10)
    
    temperature = Value("i",0)


    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX) # crée MessageQueue et renvoie une erreur si elle existe déjà
        print("Creation Message Queue")

    except sysv_ipc.ExistentialError:
        print("Message queue", key, "already exists, resetting.")
        mq = sysv_ipc.MessageQueue(key)
        mq.remove() # vide la queue
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)


    print("Demarrage MessageQueue.")

    marche = Process(target = market.market, args = (b,))
    marche.start()
    
    meteo = Process(target=weather.weather, args=(b, temperature))
    meteo.start()
    
    maisons = []

    for i in range(2): #initialise les maisons
        maison = Process(target=home.maison, args=(b,temperature))
        maisons.append(maison)
        maison.start()
    
    
    while True:
        #b.wait()
        if (fin):
            mq.remove()
            break
    
    signal.signal(signal.SIGINT, handler)

    marche.join()
    meteo.join()

    for proc in maisons :
           proc.join() #on attend la fin du proc pour le terminer
    
    shm.close()
    shm.unlink()
    mq.remove()
    print("Fin simulation")




# ici on va créer les objets et les gérer
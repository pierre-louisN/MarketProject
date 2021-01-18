#!/usr/bin/env python3 
import home
import market
import weather
from multiprocessing import Barrier, Process, shared_memory, Process, Lock, Value
import sysv_ipc
import signal
import time

fin = False

def handler(signum, frame):
    self.fin = True

if __name__== "__main__":

    key = 666

    b = Barrier(7, timeout=10) # le nombre de procs est le nombre de maisons + 4
    
    temperature = Value("i",0)


    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX) # crée MessageQueue et renvoie une erreur si elle existe déjà
        print("Creation Message Queue")

    except sysv_ipc.ExistentialError:
        print("Message queue", key, "already exists")
        try :
            mq = sysv_ipc.MessageQueue(key)
            mq.remove() # vide la queue
            print("Resetting the Message queue")
            mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
        except sysv_ipc.PermissionsError :
            print("Erreur de permission")


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
    
    while not(fin):
        time.sleep(1) #pour "ralentir l'execution"
        b.wait()
        try :
            pass
        except KeyboardInterrupt :
            fin = True
        
        if (fin):
            print("Ctrl + C attrapé par simulation")
            mq.remove()
            break
    
    signal.signal(signal.SIGINT, handler)

    marche.join()
    meteo.join()

    for proc in maisons :
           proc.join() #on attend la fin du proc pour le terminer
    
    
    mq.remove()
    print("Fin simulation")


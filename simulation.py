#!/usr/bin/env python3 
import home
import market
import weather
from multiprocessing import Barrier, Process, shared_memory, Process, Lock, Value
import multiprocessing
import sysv_ipc
import signal
import time
import threading

fin = False

def handler(signum, frame):
    self.fin = True

if __name__== "__main__":

    key = 666

    nb_maisons = 5

    b = Barrier(nb_maisons + 5, timeout=20) # le nombre de procs est le nombre de maisons + 4
    
    temperature = multiprocessing.Array('i',4) # je modifie, maintenant on un array


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
    #les maisons sont numérotés

    for i in range(nb_maisons): #initialise les maisons
        nom = "Maison n°"+str(i)
        maison = Process(target=home.maison, args=(b,temperature, nom))
        maisons.append(maison)
        maison.start()
    
    while not(fin):
        time.sleep(1) #pour "ralentir l'execution"
        try :
            b.wait()
        except threading.BrokenBarrierError :
            #print("barriere supprimé dans la simu")
            fin = True

        except KeyboardInterrupt :
            fin = True

    signal.signal(signal.SIGINT, handler)

    marche.join()
    meteo.join()

    for proc in maisons :
           proc.join() #on attend la fin du proc pour le terminer
    print("Fin Maisons")
    
    try :
        mq.remove()
    except sysv_ipc.ExistentialError:
        pass
        #print("Queue supprimé")
    print("Fin Simulation")


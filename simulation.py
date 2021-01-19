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
    fin = True

if __name__== "__main__":

    key = 666

    nb_maisons = 5 # nombre de processus maisons qui communiquent ensemble et avec market

    b = Barrier(nb_maisons + 5, timeout=20) # le nombre de processus est le nombre de maisons + 5 (market, economics, politics, simulation, weather)
    
    temperature = multiprocessing.Array('i',4) # memoire partagée de weather

    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX) # crée MessageQueue et renvoie une erreur si elle existe déjà
        print("Création Message Queue")

    except sysv_ipc.ExistentialError:
        print("Message queue", key, "existe déjà") 

        try :
            mq = sysv_ipc.MessageQueue(key)
            mq.remove() # vide la queue
            print("Reinitialisation de la Message queue")
            mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX) #en recrée une nouvelle qui est vide

        except sysv_ipc.PermissionsError :
            print("Erreur de permission, réessayer avec 'sudo'")


    print("Demarrage MessageQueue.")
    
    marche = Process(target = market.market, args = (b,))
    marche.start()
    
    meteo = Process(target=weather.weather, args=(b, temperature))
    meteo.start()
    
    maisons = []

    for i in range(nb_maisons): #initialise les maisons
        nom = "Maison n°"+str(i) # les maisons sont numérotés pour faciliter l'affichage sur le terminal
        maison = Process(target=home.maison, args=(b,temperature, nom))
        maisons.append(maison)
        maison.start()
    

    print("Début de la simulation : 365 jours maximum, Ctrl + c pour arrêter")
    while not(fin):
        try : 
            time.sleep(2) #pour "ralentir" l'execution pour laisser à l'utilisateur le temps de lire les messages des processus
            b.wait() #barrier synchronise tous les processus
        except threading.BrokenBarrierError : # la barriere a été reset donc fin de la simulation
            fin = True
        except KeyboardInterrupt : # Ctrl + C 
            fin = True

    signal.signal(signal.SIGINT, handler) #gere le signal 

    marche.join()
    meteo.join()

    for proc in maisons :
           proc.join() # on attend la fin du processus pour le terminer
    print("Fin Maisons")
    
    try :
        mq.remove()
    except sysv_ipc.ExistentialError: #la Queue a déjà été supprimé
        pass
    print("Fin Simulation")


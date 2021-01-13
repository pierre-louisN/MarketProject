#!/usr/bin/env python3
from multiprocessing import Lock,Process,Value, shared_memory
from random import *
import multiprocessing
import signal
import time



temperature = multiprocessing.Value("i")

saison = randint(1,4)

def liseur_Temp(lecture,temperature) :    # cette fonction simule ce que va faire les process home, ils vont récupérer la température et modifier leur conso
    while True :                          # quand tu la testes on a l'impression qu'elle est mauvaise parce que les procs lisent des temp différentes
        lecture = temperature.value       # mais c'est juste que les températures changent rapidement
        print(lecture)                    # pour mieux observer son fonctionnement il suffit de rajouter des time.sleep dans def meteo
    

def meteo(saison,temperature,lock):
    # on simule les saisons avec une variable saison qui augmentera après un certains nombre de signaux
    # les températures sont données de façon aléatoire selon la saison
    # les saisons changent en continue pour le moment parce qu'on a pas encore synchronisé les process avec les signaux
    while True :
        if saison == 1:
            lock.acquire()
            saison = 2
            temp = randint(-2, 6)
            temperature.value = temp
            lock.release()  
        if saison == 4:
            lock.acquire()
            saison = 1
            temp = randint(10, 14)
            temperature.value = temp
            lock.release()
        if saison == 3:
            lock.acquire()
            saison = 4
            temp = randint(25, 32)
            temperature.value = temp
            lock.release()
        if saison == 2:
            lock.acquire()
            saison = 3
            temp = randint(14, 20)
            temperature.value = temp
            lock.release()
    
 
if __name__== "__main__":

    temperature.value = 12
    lecture = randint(1,5)
    saison = 1
    
    print("Essai programme 1")
    
    lock = Lock()
    
    p1 = multiprocessing.Process(target=meteo, args=(saison,temperature,lock))
    p1.start()
    
    while True :
        print(temperature.value)
        time.sleep(2) #mettre un tick pour synchro 

    p1.join()
    
    
    
    

    

    
    
   
    
    

    
  


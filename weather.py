#!/usr/bin/env python3
from multiprocessing import Lock,Process,Value, shared_memory,Barrier
from random import *
import multiprocessing
import signal
import time


b = Barrier (1, timeout = 10)
temperature = multiprocessing.Value("i")
saison_init = 1

'''
def liseur_Temp(lecture,temperature) :    # cette fonction simule ce que va faire les process home, ils vont récupérer la température et modifier leur conso
    while True :                          # quand tu la testes on a l'impression qu'elle est mauvaise parce que les procs lisent des temp différentes
        lecture = temperature.value       # mais c'est juste que les températures changent rapidement
        print(lecture)                    # pour mieux observer son fonctionnement il suffit de rajouter des time.sleep dans def meteo
'''    

def meteo(self,saison_init,temperature,lock,barrier):
    # on simule les saisons avec une variable saison qui augmentera après un certains nombre de signaux
    # les températures sont données de façon aléatoire selon la saison
    # les saisons changent en continue pour le moment parce qu'on a pas encore synchronisé les process avec les signaux
    saison = 1
    while True :
        if saison <= 89:                    #hiver, l'hiver dure environ 89 jours
            lock.acquire()
            saison += 1
            temp = randint(-2, 6)
            temperature.value = temp
            lock.release()  
        if (saison >= 89 and saison <= 182 ):                  #printemps, il dure environ 93 jours
            lock.acquire()
            saison += 1
            temp = randint(14, 20)
            temperature.value = temp
            lock.release()
        if (saison <= 276 and saison >= 182):                   #été, il dure environ 94 jours
            lock.acquire()
            saison += 1
            temp = randint(25, 32)
            temperature.value = temp
            lock.release()
        if (saison <= 365 and saison >= 277):                   #automne, il dure environ 89 jours
            lock.acquire()
            saison += 1
            temp = randint(11, 14)
            temperature.value = temp
            lock.release()
            if saison == 365 :
                saison = 1
        barrier.wait()
    
 
if __name__== "__main__":

    temperature.value = 12
    lecture = randint(1,5)
    
    print("Essai programme 1")
    
    lock = Lock()
    
    p1 = multiprocessing.Process(target=meteo, args=(saison_init,temperature,lock,b))
    p1.start()
    
    while True :
        print(temperature.value)

    p1.join()
    
    
    
    

    

    
    
   
    
    

    
  


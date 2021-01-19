#!/usr/bin/env python3
from multiprocessing import Lock,Process,Value, shared_memory, Barrier
from random import *
import multiprocessing
import signal
import time
import threading

lock = Lock()

class weather:
    
    fin = False

    # on simule les saisons avec une variable saison qui augmente au fil du temps
    # les températures sont données de façon aléatoire selon la saison
    # les saisons changent en continue de manière synchronisé avec les autres processus
    def meteo(self,temperature, barrier):
        saison = 1
        while not(self.fin) :
            with temperature.get_lock():
                temperature [1] = 0                    #Event purement aléatoire, chaque événement a une chance sur 100 d'arriver
                if saison <= 89:                                    #hiver, l'hiver dure environ 89 jours
                    saison += 1
                    temp = randint(-2, 6)
                    temperature [0] = temp
                    temperature [1] = randint(0,49)
                if (saison >= 89 and saison <= 182 ):                  #printemps, il dure environ 93 jours
                    saison += 1
                    temp = randint(14, 20)
                    temperature [0] = temp
                if (saison <= 276 and saison >= 182):                   #été, il dure environ 94 jours
                    saison += 1
                    temp = randint(25, 32)
                    temperature [0] = temp
                    temperature [1] = randint(50,100)
                if (saison <= 365 and saison >= 277):                   #automne, il dure environ 89 jours
                    saison += 1
                    temp = randint(11, 14)
                    temperature [0] = temp
                    if saison == 365 :
                        saison = 1
            try :
                barrier.wait()
            except threading.BrokenBarrierError :
                self.fin = True
            except KeyboardInterrupt :
                self.fin = True
        
    
 
    def __init__(self, barrier, temp):
        print("Début Weather")
        
        self.meteo(temp, barrier)

        print("Fin Weather")
    
    
    
    

    

    
    
   
    
    

    
  


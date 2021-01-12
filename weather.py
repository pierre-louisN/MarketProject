from multiprocessing import Lock,Process,Value, shared_memory
from random import *
from ctypes import c_char
import multiprocessing
import signal
import time
import sys



nom = "meteo"


#année = multiprocessing.Value("i")
temperature = multiprocessing.Value("i")

saison = randint(1,4)
'''
def solstice(saison,année) :
    
    if année.value == 1 :
        saison.value = 1 ##"hiver"
        année.value = 2
    elif année.value == 2 :
        saison.value = 2 ##"printemps"
        time.sleep(2)
        année.value = 3
    elif année.value == 3 :
        saison.value = 3 ##"été"
        time.sleep(2)
        année.value = 4
    elif année.value == 4 :
        saison.value = 4 ##"automne"
        time.sleep(2)
        année.value = 1
'''
def meteo(saison,temperature,lock):
    # on simule les saisons avec une variable saison qui augmentera après un certains nombre de signaux
    # les températures sont données de façon aléatoire selon la saion
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
    #année.value = 1 
    saison = 1
    print("Essai programme 1")
    lock = Lock()
    p1 = multiprocessing.Process(target=meteo, args=(saison,temperature,lock))
    p2 = multiprocessing.Process(target=meteo,args=(saison,temperature,lock))
            
    p1.start()
    print(temperature.value)
    p2.start()
    print(temperature.value)
    mem = shared_memory.ShareableList([10],name="mem_meteo")

    while True :
        print(mem.shm.name)
        sleep(2) #mettre un tick pour synchro 

    
    mem.shm.close()
    mem.shm.unlink()

    
    
   
    
    

    
  


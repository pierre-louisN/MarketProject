from multiprocessing import Lock,Process,Value
from random import *
from ctypes import c_char
import multiprocessing
import signal
import time



nom = "meteo"


année = multiprocessing.Value("i")
temperature = multiprocessing.Value("i")
saison = multiprocessing.Value("i")

def solstice(saison,année) :
    
    if année.value == 1 :
        saison.value = 1 ##"hiver"
        time.sleep(2)
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

def meteo(saison,temperature,lock):
    if saison.value == 1:
        lock.acquire()
        temp = randint(-2, 6)
        temperature.value = temp
        lock.release()  
    if saison.value == 4:
        lock.acquire()
        temp = randint(10, 14)
        temperature.value = temp
        lock.release()
    if saison.value == 3:
        lock.acquire()
        temp = randint(25, 32)
        temperature.value = temp
        lock.release()
    if saison.value == 2:
        lock.acquire()
        temp = randint(14, 20)
        temperature.value = temp
        lock.release()
    time.sleep(2)
 
if __name__== "__main__":

    temperature.value = 12
    année.value = 1 
    saison.value = 1
    print("Essai programme 1")
    lock = Lock()
    while True :
        p1 = multiprocessing.Process(target=solstice, args=(saison,année))
        p2 = multiprocessing.Process(target=meteo,args=(saison,temperature,lock))
        
        
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    
        print(temperature.value)
        time.sleep(2)
    
    

    
  


from multiprocessing import Lock,Process,Value
from random import *
import multiprocessing
import signal
import time



nom = "meteo"

saison = "hiver" #je pense qu'il faudrait rajouter une variable saison qui se moidifierait de façon chronique 
                 #histoire de baser la météo dessus et pour recréeer des saisons

temperature = multiprocessing.Value("i")

def meteo(saison,temperature,lock):
    if saison == "hiver":
        lock.acquire()
        temp = randint(-2, 6)
        temperature.value = temp
        lock.release()  
    if saison == "automne":
        lock.acquire()
        temp = randint(10, 14)
        temperature.value = temp
        lock.release()
    if saison == "été":
        lock.acquire()
        temp = raisendint(25, 32)
        temperature.value = temp
        lock.release()
    if saison == "printemps":
        lock.acquire()
        temp = randint(14, 20)
        tempertature.value = temp
        lock.release()
 
if __name__== "__main__":

    
    print("Essai programme 1")
    lock = Lock()
    while True :
        p1 = multiprocessing.Process(target=meteo,args=(saison,temperature,lock))
    
        p1.start()
        p1.join()
    
        print(temperature.value)
        time.sleep (5)
    
    

    
  


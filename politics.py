from multiprocessing import Lock,Process,Value
from random import *
from ctypes import c_char
import multiprocessing
import signal
import time

evenement = multiprocessing.Array('i')
listEvenement = [guerre,dictature,anarchie]
guerre = False
dictature = False
anarchie = False

def Event(evenement,aleat):
    evenement.value = aleat
    if evenement.value == 9 :
        guerre = True
    elif evenement.value == 3 :
        dictature = True 
    elif evenement.value == 0 : 
        anarchie = True
    

if __name__ == "__main__" :
    
    aleat = randint(1,10)
    p1 = multiprocessing.Process(target=Event , args = (evenement, aleat))
    p2 = multiprocessing.Process(target=Event , args = (evenement, aleat))
    
    p1.start()
    p1.join()
    
    print(evenement.value)
    print(guerre)
    print(dictature)
    print(anarchie)
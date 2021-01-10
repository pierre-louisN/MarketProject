from multiprocessing import Lock,Process,Value
from random import *
from ctypes import c_char
import multiprocessing
import signal
import time

evenement = multiprocessing.Value('i')
crash_fincancier = False
dictature = False
anarchie = False

def Event(evenement,aleat):
    evenement.value = aleat
    if evenement.value == 9 :
        crash_fincancier = True
    elif evenement.value == 13 :
        dictature = True 
    elif evenement.value == 0 : 
        anarchie = True
    

if __name__ == "__main__" :
    
    aleat = randint(1,20)
    p1 = multiprocessing.Process(target=Event , args = (evenement, aleat))
    p2 = multiprocessing.Process(target=Event , args = (evenement, aleat))
    
    p1.start()
    p1.join()
    
    print(evenement.value)
    print(crash_fincancier)
    print(dictature)
    print(anarchie)
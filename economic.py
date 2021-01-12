from multiprocessing import Lock,Process,Value
from random import *
from ctypes import c_char
import multiprocessing
import signal
import time

evenement = randint(1,40)
crash_fincancier = False
dictature = False
anarchie = False

def Event(evenement):
    #Il y a 3 évènements possibles, à chaque synchronisation on lance un randint 
    #Si le randint correspond à l'un des évènement : il devient vrai
    if evenement == 9 :
        crash_fincancier = True
    elif evenement == 13 :
        dictature = True 
    elif evenement == 0 : 
        anarchie = True
    

if __name__ == "__main__" :
    
    p1 = multiprocessing.Process(target=Event , args = (evenement))
    p2 = multiprocessing.Process(target=Event , args = (evenement))
    
    p1.start()
    p1.join()
    
    print(evenement.value)
    print(crash_fincancier)
    print(dictature)
    print(anarchie)
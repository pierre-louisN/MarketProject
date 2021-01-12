from multiprocessing import Lock,Process,Value,Pipe
from random import *
import multiprocessing
import sys
import os

evenement = randint(1,40)
crash_fincancier = False
dictature = False
anarchie = False

#Création du pipe
parent_conn, child_conn = Pipe()


def Event(evenement):
    #Il y a 3 évènements possibles, à chaque synchronisation on lance un randint 
    #Si le randint correspond à l'un des évènement : il devient vrai
    while True :
        evenement = randint (1,400)
        if evenement == 9 :
            crash_fincancier = True
            child_conn.send("crash_fincancier")#prévient le père
        elif evenement == 13 :
            dictature = True
            child_conn.send("dictature")#prévient le père
        elif evenement == 0 : 
            anarchie = True
            child_conn.send("anarchie")#prévient le père

if __name__ == "__main__" :
    
    p1 = multiprocessing.Process(target=Event , args = (evenement))
    
    
    p1.start()
    p1.join()
    
    print(evenement.value)
    print(crash_fincancier)
    print(dictature)
    print(anarchie)
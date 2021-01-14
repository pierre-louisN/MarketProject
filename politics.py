#!/usr/bin/env python3
import sys
import os
from random import *
import multiprocessing
from multiprocessing import Process, Barrier, Pipe 


class politics :
    evenement_P = randint(1,400)
    guerre = False
    dictature = False
    anarchie = False
    listEvenementPolitics = [guerre,dictature,anarchie] #on peut faire une fonction qui lit ce tableau continuellement
    b = Barrier(1, timeout=10)

    #Création du pipe2
    parent_conn2, child_conn2 = Pipe()

    def Event(self,evenement_P,child_conn2,barrier):
        while True :
            evenement_P = randint(1,400)
            if evenement_P == 9 :
                guerre = True
                child_conn2.send("guerre")#prévient le père
            elif evenement_P == 3 :
                dictature = True
                child_conn2.send("dictature")#prévient le père            
            elif evenement_P == 0 : 
                anarchie = True
                child_conn2.send("anarchie")#prévient le père
            barrier.wait()
if __name__ == "__main__" :
        
    p1 = multiprocessing.Process(target=Event , args = (evenement_P, child_conn2,b))
  
    p1.start()
    p1.join()
    
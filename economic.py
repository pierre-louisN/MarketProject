#!/usr/bin/env python3
from multiprocessing import Lock,Process,Value,Pipe
from random import *
import multiprocessing
import sys
import os
from random import *
import multiprocessing
from multiprocessing import Process, Barrier, Pipe 


class economic :
    evenement_E = 3421
    crash_fincancier = False
    inflation = False
    anarchie  = False
    listEvenementEconomics = [ crash_fincancier, inflation, anarchie ] #on peut faire une fonction qui lit ce tableau en boucle, et dès qu'il voit true agit
    b = Barrier(1, timeout=10)
    #Création du pipe
    parent_conn, child_conn = Pipe()

    def Event(self,evenement_E, child_conn,barrier):
        #Il y a 3 évènements possibles, à chaque synchronisation on lance un randint 
        #Si le randint correspond à l'un des évènement : il devient vrai
        while True :
            evenement_E = randint(1,4000)#les évènements ont une chance sur 200 d'arriver
            if evenement_E == 921 :
                crash_fincancier = True
                child_conn.send("crash_fincancier")#prévient le père
            elif evenement_E == 123 :
                inflation = True
                child_conn.send("inflation")#prévient le père
            elif evenement_E == 3900 : 
                anarchie = True
                child_conn.send("anarchie")#prévient le père
            barrier.wait()
 '''  
if __name__ == "__main__" :
    
    p1 = multiprocessing.Process(target=Event , args = (evenement_E,child_conn,b))
    
    p1.start()
    p1.join()
'''
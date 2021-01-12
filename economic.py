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


def Event(evenement, child_conn):
    #Il y a 3 évènements possibles, à chaque synchronisation on lance un randint 
    #Si le randint correspond à l'un des évènement : il devient vrai
    while True :
        evenement = randint(1,200)#les évènements ont une chance sur 200 d'arriver
        if evenement == 9 :
            crash_fincancier = True
            child_conn.send("crash_fincancier")#prévient le père
            print(parent_conn.recv())#c'était pour vérifier si le pipe fonctionnait correctement, j'ai fais un test en fixant evenement à 9
        elif evenement == 13 :
            dictature = True
            child_conn.send("dictature")#prévient le père
        elif evenement == 100 : 
            anarchie = True
            child_conn.send("anarchie")#prévient le père

        
if __name__ == "__main__" :
    
    p1 = multiprocessing.Process(target=Event , args = (evenement,child_conn))
    
    p1.start()
    p1.join()

#test market + politics + economics
import os
import sys
from random import *
import time
import sysv_ipc
import multiprocessing
from multiprocessing import Pipe, Process 
import concurrent.futures

evenement_P = randint(1,400)
guerre = False
dictature = False
anarchie = False
listEvenementPolitics = [guerre,dictature,anarchie]


evenement_E = randint(1,400)
crash_fincancier = False
inflation = False
crise_financière  = False
listEvenementEconomics = [ crash_fincancier, inflation, crise_financière ]

key = 666

#Création du pipe1
parent_conn, child_conn = Pipe()

def Event_E(evenement_E, child_conn):
    #Il y a 3 évènements possibles, on lance en boucle un randint 
    #Si le randint correspond à l'un des évènement : il devient vrai
    while True :
        evenement_E = 100 #test!!!
        #evenement_E = randint(1,400)#les évènements ont une chance sur 200 d'arriver
        if evenement_E == 9 :
            crash_fincancier = True
            child_conn.send("crash_fincancier")#prévient le père
        elif evenement_E == 13 :
            inflation = True
            child_conn.send("inflation")#prévient le père
        elif evenement_E == 100 : 
            crise_financière = True
            child_conn.send("crise_financière")#prévient le père
            
            
            
#Création du pipe2
parent_conn2, child_conn2 = Pipe()

def Event_P(evenement_P,child_conn2):
    while True :
        evenement_P = 0
        #evenement = randint(1,400)
        if evenement_P == 9 :
            guerre = True
            child_conn2.send("guerre")#prévient le père
        elif evenement_P == 3 :
            dictature = True
            child_conn2.send("dictature")#prévient le père            
        elif evenement_P == 0 : 
            anarchie = True
            child_conn2.send("anarchie")#prévient le père
            

def worker(mq, m, t, cout): #gére  les transactions avec les maisons
    if t == 4 : # vente
        print("Maison veut vendre",int(m),"d'energie")
        cout  = cout - (int(m) * 0.01) # plus d'énergie disponible donc le prix baisse
    if t == 5 : # achat
        print("Maison veut acheter",int(m),"d'energie")
        print("Marché fait la transaction") # es ce que c'est nécessaire d'envoyer quelque chose dans la queue ici ?
        cout = cout + (int(m) * 0.01) # moins d'énergie disponible donc le prix augmente
    return cout

def listener (parent_conn,parent_conn2):
    while True :
        message_E = parent_conn.recv() 
        message_P = parent_conn2.recv()
        print(message_E)
        print(message_P)
        
 
if __name__ == "__main__":
    '''
   try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)

    except sysv_ipc.ExistentialError:
        print("Message queue", key, "already exists, connecting.")
        mq = sysv_ipc.MessageQueue(key)

    print("Demarrage MessageQueue.")

    with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor: #limite  de 10 pour gérer les transactions avec les maisons
        cout = 1 # cout de l'energie
        while True:
            m, t = mq.receive(True)
            calc = executor.submit(worker, mq, m, t, cout)
            cout = calc.result()
            print("prix actuelle de l'energie est",cout)
            if cout > 10 :
                print("Crise économique") # on va signaler economics
            if t == 6 :
                mq.remove()
                ('Fin du processus home')

        mq.remove()

    print("Fin Market.")
    '''
    p1 = multiprocessing.Process(target=Event_E , args = (evenement_E, child_conn))
    p2 = multiprocessing.Process(target=Event_P , args = (evenement_P, child_conn2))
    p3 = multiprocessing.Process(target=listener , args = (parent_conn,parent_conn2))
    
    p1.start()
    p2.start()
    p3.start()
    
    p1.join()
    p2.join()
    p3.join()
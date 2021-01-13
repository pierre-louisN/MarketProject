import sys
import os

evenement_P = randint(1,400)
guerre = False
dictature = False
anarchie = False
listEvenementPolitics = [guerre,dictature,anarchie] #on peut faire une fonction qui lit ce tableau continuellement

#Création du pipe2
parent_conn2, child_conn2 = Pipe()

def Event(evenement,child_conn2):
    while True :
        evenement = randint(1,400)
        if evenement == 9 :
            guerre = True
            child_conn2.send("guerre")#prévient le père
        elif evenement == 3 :
            dictature = True
            child_conn2.send("dictature")#prévient le père            
        elif evenement == 0 : 
            anarchie = True
            child_conn2.send("anarchie")#prévient le père
    
if __name__ == "__main__" :
        
    p1 = multiprocessing.Process(target=Event , args = (evenement, child_conn2))
  
    p1.start()
    p1.join()
    
   
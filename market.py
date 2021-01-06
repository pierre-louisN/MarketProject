import sys
import time
import sysv_ipc
import concurrent.futures

key = 666

def worker(mq, m): #gére  les transactions avec les maisons
    print("message recu",m)


if __name__ == "__main__":
    try:
        mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREX)
    except ExistentialError:
        print("Message queue", key, "already exsits, terminating.")
        sys.exit(1)

    print("Demarrage MessageQueue.")

    with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor: #gére les transactions avec home
        while True:
            m, t = mq.receive()
            if t == 1: #achat 
                executor.submit(worker, mq, m)
            if t == 2:
                mq.remove()
                break


    print("Fin MessageQueue.")

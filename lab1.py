import numpy as np
import threading
import time
import multiprocessing
import queue
size = 100
matA=np.random.randint(10,size=(size,size))
matB=np.random.randint(10,size=(size,size))
result=np.zeros((matA.shape[0], matB.shape[1]))

def matrix(row,size):
    splpart= int(size/10)
    for splitrow in range(row*splpart, splpart*row+splpart):
        result[splitrow] = np.matmul(matA[splitrow], matB)

def thread_func(row, result_queue):
    splpart= int(size/10)
    for splitrow in range(row*splpart, splpart*row+splpart):
        result[splitrow] = np.matmul(matA[splitrow], matB)
    print(result)
    result_queue.put(result)


def main():
    start_time = time.time()
    thread_num = 10 # How many thread you want to use
    threads = []

    # Assign job to threads
    for i in range(thread_num):
        # Pass argument to function with tuple
        thread = threading.Thread(target = matrix, args = (i,size)) #args就是需要輸入thread_func的變數
        threads.append(thread)

    # run all threads
    for thread in threads:
        thread.start()

    # Wait for threads finish
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print('Answer is correct:', np.all(np.matmul(matA, matB) == result))
    print('Time elapsed by Thread:\t', end_time - start_time)

def pro():
    # Generate queue for communication
    start_time = time.time()
    result_queue = multiprocessing.Manager().Queue()

    processes = 10
    jobs = []

    for i in range(processes):
        process = multiprocessing.Process(target = thread_func, args = (i, result_queue))
        jobs.append(process)

    for process in jobs:
        process.start()

    for process in jobs:
        process.join()

    while not result_queue.empty():
        result = result_queue.get()
    end_time = time.time() 
    print('Answer is correct:', np.all(np.matmul(matA, matB) == result))
    print('Time elapsed by Thread:\t', end_time - start_time)
if __name__ == "__main__":
    main()
    pro()
#print(result)


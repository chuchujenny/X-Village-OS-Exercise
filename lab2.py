#https://www.cnblogs.com/itogo/p/5635629.html
#https://docs.lvrui.io/2016/07/20/Python%E4%B8%AD%E5%85%88%E8%BF%9B%E5%85%88%E5%87%BA%E9%98%9F%E5%88%97queue%E7%9A%84%E5%9F%BA%E6%9C%AC%E4%BD%BF%E7%94%A8/
import threading
import queue
import os
import time

buffer_size = 5
lock = threading.Lock()          #put()存入;get()取出
queue = queue.Queue(buffer_size) #Queue是python标准库中的线程安全的队列（FIFO）实现,提供了一个适用于多线程编程的先进先出的数据结构，即队列，用来在生产者和消费者线程之间的信息传递
file_count = 0

#os.path.join('aaaa','./bbb','ccccc.txt') 輸出 aaaa\./bbb\ccccc.txt

def producer(top_dir, queue_buffer):
    # Search sub-dir in top_dir and put them in queue 
    queue_buffer.put(top_dir)
    time.sleep(1/2)
    #print(queue_buffer.qsize())
    #print(top_dir)
    a=os.listdir(top_dir)  
    for i in range(len(a)):
        filepath = os.path.join(top_dir,a[i])
        if os.path.isdir(filepath):
                #queue_buffer.put(filepath)
            producer(filepath,queue)
            continue
        else:
            pass
        
#多研究關於在裡面加lock的執行
def consumer(queue_buffer):
    # search file in directory
    global file_count
    while  not queue_buffer.empty():
        subfile=queue_buffer.get()
        time.sleep(1)
        b=os.listdir(subfile)
        for i in range(len(b)):
            subfilepath = os.path.join(subfile,b[i])
            if os.path.isfile(subfilepath):
                file_count +=1
            else:
                pass

def main():
    producer_thread = threading.Thread(target = producer, args = ('./testdata', queue))

    consumer_count = 20
    consumers = []
    for i in range(consumer_count):
        consumers.append(threading.Thread(target = consumer, args = (queue,)))

    producer_thread.start()
    for c in consumers:
        c.start()

    producer_thread.join()
    for c in consumers:
        c.join()                        #join()為阻塞调用线程，直到队列中的所有任务被处理掉。

    print(file_count, 'files found.')

if __name__ == "__main__":
    main()

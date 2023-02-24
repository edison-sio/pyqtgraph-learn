from multiprocessing import Process, Queue
import time

def process_one(data: Queue):
    for i in range(10):
        data.put(i)
        time.sleep(0.1)

def process_two(data: Queue):
    while True:
        ele = data.get()
        if ele:
            print(ele)
        print('keep going')

if __name__ == '__main__':
    data = Queue()
    p1 = Process(target=process_one, args=(data,))
    p2 = Process(target=process_two, args=(data,))

    p1.start()
    p2.start()

    time.sleep(2)
    p1.join()
    p2.terminate()

    p1.start()
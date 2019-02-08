import asyncio
# from _thread import *
import threading
import numpy as np
import random
import time
import socket 

# extemp_IP = '172.20.10.3' #192.168.137.74
# extemp_PORT = 5005
# extemp_address = (extemp_IP, extemp_PORT)

# try:
#     extemp_sock.bind(extemp_address)
# except socket.error as e: 
#     print(str(e))


sensor_data_buff = np.zeros((1,6))
lock = asyncio.Lock()
b_lock = threading.Lock()
sensor_data_buff = np.zeros((3,6))
# weights = np.random.dirichlet(np.ones(6), size=1)
vol_range = 50
min_volume = 40
tempo_range = 60
min_tempo = 60
num_devices = 3
lock = asyncio.Lock()
num_updates = 0
threads = []

def client_routine(id):
    global b_lock
    global sensor_data_buff
    global num_updates
    string_data = "1 1 -1 1 -1 1"
    while True: 
        data = string_data.split(" ")
        data = list(map(int, data))
        data = np.absolute(data)
        while(not b_lock.acquire(blocking=True)):
            time.sleep(random.randint(1,5))
        sensor_data_buff[id] =  np.array(data)
        print(sensor_data_buff[id])
        num_updates += 1
        b_lock.release()
        time.sleep(5)
    # global sensor_data_buff
    # time.sleep(1)
    # with a_lock:
    #     print("lock acquired"+str(id))
    #     sensor_data_buff = sensor_data_buff + np.array([1,1,1,1,1,1])
    #     print(str(id)+": id")
    #     print(sensor_data_buff)

def calcParam(connection):
    global sensor_data_buff
    global b_lock
    global threads
    global num_updates
    # weights = np.random.dirichlet(np.ones(6), size=1)
    num_devices = 3 #len(threads)
    while True:
        if(num_updates > num_devices):
            # while(not b_lock.acquire(blocking=True)):
            #     time.sleep(random.randint(1,5))
            accum_data = sensor_data_buff.sum(axis=0)
            # sensor_data_buff = sensor_data_buff * weights
            print(accum_data)
            # sensor_data_buff = np.zeros((1,6))
            num_updates = 0
            print("sending to extmp extention...")
            # first integer is tempo and the second it volume.
            connection.send('75 60'.encode())
            # b_lock.release()

def taskGenerator():
    for i in range(3):
        print("creating task")
        c_thread = threading.Thread(target=client_routine, args=(i,))
        threads.append(c_thread)
        c_thread.start()

    print("num of threads: "+str(len(threads)))
        # asyncio.ensure_future(client_routine(i))

async def initiate_session():
    print("Creating coroutine...")
    # cor1 = asyncio.ensure_future(client_routine())
    # cor2 = asyncio.ensure_future(client_routine())
    # await asyncio.wait(client_routine(websocket))

# start_new_thread(lala, (1, ))
taskGenerator()

extemp_IP = '130.56.77.72' #'10.20.122.238' #172.20.10.3' #192.168.137.74
extemp_PORT = 5005
extemp_address = (extemp_IP, extemp_PORT)
extemp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    extemp_sock.bind(extemp_address)
except socket.error as e: 
    print(str(e))
# extemp_sock.connect(extemp_address)
print("Socket bound")
extemp_sock.listen(1)
while True: 
    connection, address = extemp_sock.accept()
    p_thread = threading.Thread(target=calcParam, args=(connection, ))
    p_thread.start()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(taskGenerator())
import asyncio
# from _thread import *
import threading
import websockets
import numpy as np
import random
import time
import socket 

sensor_IP = '172.20.10.3' #192.168.137.74
sensor_PORT = 8882
num_queued_msgs = 2
address = (sensor_IP, sensor_PORT)
# weights = np.random.dirichlet(np.ones(6), size=1)
vol_range = 50
min_volume = 40
tempo_range = 60
min_tempo = 60
num_devices = 3
# lock = asyncio.Lock()
num_updates = 0
device_id = 0

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

def client_routine(id, connection):
    # global b_lock
    print("in new client thread")
    global sensor_data_buff
    global num_updates
    string_data = "1 1 -1 1 -1 1"
    while True: 
        data = connection.recv(1024)
        if(not str(data.decode())==''):
            print(str(id)+" received data "+str(data.decode()))
        data = string_data.split(' ')
        data = list(map(int, data))
        data = np.absolute(data)
        # while(not b_lock.acquire(blocking=True)):
        #     time.sleep(random.randint(1,5))
        ######### sensor_data_buff[id] =  np.array(data)
        # print(sensor_data_buff[id])
        num_updates += 1
    connection.close()
        # b_lock.release()
    # global sensor_data_buff
    # time.sleep(1)
    # with a_lock:
    #     print("lock acquired"+str(id))
    #     sensor_data_buff = sensor_data_buff + np.array([1,1,1,1,1,1])
    #     print(str(id)+": id")
    #     print(sensor_data_buff)

def calcParam(connection):
    global sensor_data_buff
    # global b_lock
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

def newDeviceConn(connection, address, id):
    global device_id
    c_thread = threading.Thread(target=client_routine, args=(id,connection))
    threads.append(c_thread)
    c_thread.start()
    print("started new device thread on address: "+str(address))
    device_id += 1

# start_server = websockets.serve(newDeviceConn, sensor_IP, sensor_PORT)

extemp_IP = '172.20.10.3' #'10.20.122.238' #172.20.10.3' #192.168.137.74
extemp_PORT = 5005
extemp_address = (extemp_IP, extemp_PORT)
extemp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    extemp_sock.bind(extemp_address)
except socket.error as e: 
    print(str(e))
# extemp_sock.connect(extemp_address)
print("Extmp socket bound")
extemp_sock.listen(1)
sensor_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sensor_sock.bind((sensor_IP, sensor_PORT))
except socket.error as e: 
    print(str(e))
print("Sensor socket bound")
sensor_sock.listen(1)
sensor_connected = False
connections = 0
while not sensor_connected:
    print("listening for sensors...")
    connection, address = sensor_sock.accept()
    connections += 1
    newDeviceConn(connection, address, connections)
    sensor_connected = True

print("sensor connection successful")
extemp_connected = False
while not extemp_connected: 
    connection, address = extemp_sock.accept()
    p_thread = threading.Thread(target=calcParam, args=(connection, ))
    p_thread.start()
    extemp_connected = True
# loop = asyncio.get_event_loop()
# loop.run_until_complete(taskGenerator())
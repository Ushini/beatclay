import asyncio
# from _thread import *
import threading
import websockets
import numpy as np
import random
import time
import socket 

server_IP = '172.20.10.3' 
sensor_PORT = 8882
address = (server_IP, sensor_PORT)
vol_range = 50
min_volume = 40
tempo_range = 60
min_tempo = 60
max_num_devices = 3
num_connections = 0
# num_updates = 0
# device_id = 0
# weights = np.random.dirichlet(np.ones(6), size=1)
sensor_data_buff = np.zeros((3,6))
threads = []
sensor_connected = False
extemp_PORT = 5005
extemp_address = (server_IP, extemp_PORT)
extemp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sensor_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def client_routine(id, connection):
    print("in new client thread")
    global sensor_data_buff
    while True: 
        data = connection.recv(1024)
        if(not str(data.decode())==''):
            print(str(id)+" received data "+str(data.decode()))
        # should this be in a try catch
            data = data.decode().strip().split(" ")
            data = np.array([float(i) for i in data]) #np.array(list(map(float, data)))
            data = np.absolute(data)
            sensor_data_buff[id] = data
    connection.close()

def calcParam(connection):
    global sensor_data_buff
    global threads
    global num_connections
    global vol_range
    global min_volume
    global tempo_range 
    global min_tempo
    max_accel = 16
    max_gyro = 2000
    # weights = np.random.dirichlet(np.ones(6), size=1)
    while True:
        if(not num_connections == 0):
            time.sleep(5)
            accum_data = sensor_data_buff.sum(axis=0)
            tempo_array = accum_data[0:3]/max_accel
            volume_array = accum_data[3:6]/max_gyro
            new_tempo = int(tempo_range*np.amax(tempo_array))+min_tempo
            new_vol = int(vol_range*np.amax(volume_array))+min_volume
            param_data = str(new_tempo)+" "+str(new_vol)
            print("sending to extmp extention...")
            # first integer is tempo and the second it volume.
            connection.send(param_data.encode())

def newDeviceConn(connection, address, id):
    c_thread = threading.Thread(target=client_routine, args=(id,connection))
    threads.append(c_thread)
    c_thread.start()
    print("started new device thread on address: "+str(address))

# start_server = websockets.serve(newDeviceConn, sensor_IP, sensor_PORT)


try:
    extemp_sock.bind(extemp_address)
except socket.error as e: 
    print(str(e))
print("Extmp socket bound")
extemp_sock.listen(1)

try:
    sensor_sock.bind((server_IP, sensor_PORT))
except socket.error as e: 
    print(str(e))
print("Sensor socket bound")
sensor_sock.listen(max_num_devices)

print("sensor connection successful")
extemp_connected = False
while not extemp_connected: 
    connection, address = extemp_sock.accept()
    p_thread = threading.Thread(target=calcParam, args=(connection, ))
    p_thread.start()
    extemp_connected = True

while True:
    print("listening for sensors...")
    connection, address = sensor_sock.accept()
    newDeviceConn(connection, address, num_connections)
    num_connections += 1

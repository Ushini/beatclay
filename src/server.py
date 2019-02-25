'''
Copyright 2019 Ushini Attanayake

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT 
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import threading
import sys
import numpy as np
import random
import time
import socket 

server_IP = sys.argv[1] 
sensor_PORT = sys.argv[2] 
address = (server_IP, sensor_PORT)
vol_range = 50
min_volume = 50
tempo_range = 60
min_tempo = 60
max_num_devices = 3
num_connections = 0

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
            data = data.decode()
            data = data.strip().split(" ")
            data = data[0:6]
            data = np.array([int(i) for i in data]) 
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
    max_accel = 20000
    max_gyro = 10000
    
    while True:
        if(not num_connections == 0):
            time.sleep(random.randint(0,5))
            accum_data = np.divide(sensor_data_buff.sum(axis=0), 3)
            accel_array = np.divide(np.absolute(accum_data[0:3]), max_accel)
            gyro_array = np.divide(accum_data[3:6], max_gyro)
            new_tempo = num_connections*int(tempo_range*np.amax(accel_array))/3+min_tempo
            if(np.absolute(np.amin(gyro_array)) > np.amax(gyro_array)):
                new_vol = num_connections*int(vol_range*np.amin(gyro_array))/3+min_volume
            else:
                new_vol = int(vol_range*np.amax(gyro_array))+min_volume
            param_data = str(new_tempo)+" "+str(new_vol)
            print("sending to extmp extention... "+str(new_tempo)+" "+str(new_vol))
            # first integer is tempo and the second is volume.
            connection.send(param_data.encode())

def newDeviceConn(connection, address, id):
    c_thread = threading.Thread(target=client_routine, args=(id,connection))
    threads.append(c_thread)
    c_thread.start()
    print("started new device thread on address: "+str(address))

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

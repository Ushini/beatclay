import requests
# import socket 
# from _thread import *

# UDP_IN_IP = '192.168.56.1' #192.168.137.74
# UDP_PORT = 80
# num_queued_msgs = 2
# address = (UDP_IN_IP, UDP_PORT)

# def new_client_thread(client, address):
#     print("in new  client thread: "+str(addr))
#     while True:
#         data = client.recv(1024)
#         if not data: 
#             break
#         print(data)
#     client.close()
#     return None

# server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# try:
#     server_sock.bind(address)
# except socket.error as e: 
#     print(str(e))

# server_sock.listen(num_queued_msgs)
# print("listening for messages...")

# # whenever a message is received from the client, create a new thread on 
# # which the agent can serve (return a new pattern string)
# while True: 
#     client, addr = server_sock.accept()
#     print('connected to: '+addr[0]+':'+str(addr[1]))
#     client.send(str.encode("CNCT")) # confirm connection
#     start_new_thread(new_client_thread, (client, addr))


response = requests.get("http://192.168.56.1/Python")
print(response.text)
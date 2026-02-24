import socket

import cv2
import time
import easygopigo3 as easy
#from picamera import PiCamera

targetIP = '0.0.0.0'

# Create the socket and wait for the initial client connection
server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((targetIP, 6100))

server_socket.listen(1)
print("Waiting for connection...")
conn, addr = server_socket.accept()
print(f" Connect by {addr}")

# Send message to client
while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f"Received: {data.decode()}")
    conn.send(b"Echo: " + data)
    break

conn.close()
server_socket.close()
import socket

import cv2
import time
import easygopigo3 as easy
from picamera import PiCamera

my_gopigo = easy.EasyGoPiGo3()

targetIP = '0.0.0.0'

# Data size used when transfering image in bytes
datasize = 1024

# Create the socket and wait for the initial client connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((targetIP, 6100))

server_socket.listen(1)
print("Waiting for connection...")
conn, addr = server_socket.accept()
print(f" Connect by {addr}")

with PiCamera() as camera:
    camera.resolution = (640,480)
    camera.start_preview()
    camera.capture('image.jpg')
    
    f = open('image.jpg','rb')
    packet = f.read(datasize)

    # Send message to client
    data = conn.recv(1024)
    print(f"Received: {data.decode()}")
    conn.send(b"Echo: " + data)
    while packet:
        conn.send(packet)
        packet = f.read(datasize)
    print(f"image sent")
    f.close()

# Wait for the client action
action = socket.recv(10)
print(f"Receive the action: {action}")

# Act according to client instructions
if action == "S":
    print("Moving forward 10 inches")
    my_gopigo.drive_cm(10)
if action == "R":
    print("Turning 45 degrees and moving forward 10 inches")
    my_gopigo.turn_degrees(45)
    my_gopigo.drive_cm(10)
if action == "L":
    print("Turning -45 degrees and moving forward 10 inches")
    my_gopigo.turn_degrees(-45)
    my_gopigo.drive_cm(10)
if action == "LL":
    print("Turning 45 degrees to locate target")
    my_gopigo.turn_degrees(45)
    my_gopigo.drive_cm(10)

conn.close()
server_socket.close()
camera.close()
import socket

import cv2
import time
import easygopigo3 as easy
from picamera import PiCamera

my_gopigo = easy.EasyGoPiGo3()

targetIP = '0.0.0.0'

# Data size used when transfering image in bytes
datasize = 1024

with PiCamera() as camera:
    camera.resolution = (640,480)

    # Create the socket and wait for the initial client connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((targetIP, 6200))

    server_socket.listen(1)
    print("Waiting for connection...")
    conn, addr = server_socket.accept()
    print(f" Connect by {addr}")

    while True:
        
        #camera.start_preview()
        camera.capture('image.jpg')

        f = open('image.jpg','rb')
        packet = f.read(datasize)

        # Send image to client
        while packet:
            conn.send(packet)
            packet = f.read(datasize)
        conn.shutdown(socket.SHUT_WR) # Signal no more data
        print(f"image sent")
        f.close()
        conn.close()
        #server_socket.close()
        # IMPORTANT: Conection closes on the server side due to indicate that the
            #file was transfered. We could not find a better way to go about it.

        # Re-create the socket and wait for the initial client connection
        #server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server_socket.bind((targetIP, 6800))

        #server_socket.listen(1)
        print("Waiting for connection...")
        conn, addr = server_socket.accept()
        print(f" Connect by {addr}")


        # Wait for the client action
        action = conn.recv(10).decode()
        print(f"Receive the action: {action}")
        #conn.close()

        # Act according to client instructions
        if action == "S":
            print("Moving forward 15 inches")
            my_gopigo.drive_cm(15)
        if action == "R":
            print("Turning 30 degrees and moving forward 15 inches")
            my_gopigo.turn_degrees(30)
            my_gopigo.drive_cm(15)
        if action == "L":
            print("Turning -30 degrees and moving forward 15 inches")
            my_gopigo.turn_degrees(-30)
            my_gopigo.drive_cm(15)
        if action == "T":
            print("Turning 30 degrees to locate target")
            my_gopigo.turn_degrees(30)
        if action == "D":
            conn.close()
            break

#conn.close()
#server_socket.close()
camera.close()
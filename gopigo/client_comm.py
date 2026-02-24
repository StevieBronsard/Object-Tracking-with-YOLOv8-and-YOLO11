#Client
import socket

# Target IP of the Gopigo robot
targetIP = '10.10.10.10'

# Data size used when transfering image in bytes
datasize = 1024

# File to store the picture of the foward view
captureFile = r"C:\Users\s22br\Documents\gopigo\pics\capture.jpg"
f = open(captureFile, 'wb')

print("Starting the connection")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((targetIP, 6100))
print("Waiting for the image...")


# Start timer
'''while True:'''
response = client_socket.recv(datasize)

while response:
    f.write(response)
    response = client_socket.receive(datasize)
f.close

print(f"image received")

# We now let our object detection model analyze the image and decide a course of action


client_socket.send('q')

client_socket.close()
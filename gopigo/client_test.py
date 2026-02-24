#Client
import socket

# Target IP of the Gopigo robot
targetIP = '10.10.10.10'

# Data size used when transfering image in bytes
datasize = 1024

# File to store the picture of the foward view
captureFile = r"C:\Users\s22br\Documents\gopigo\pics\capture.jpg"
f = open(captureFile, 'wb')

print(f"Starting the connection")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((targetIP, 6100))
print(f"Sending the message")

client_socket.send("Hello World!".encode())
print(f"message sent")
data = client_socket.recv(datasize)
print(f"Received: {data.decode()}")
print(f"message received")

data = client_socket.recv(datasize)

while data:
    f.write(data)
    data = client_socket.recv(datasize)
print(f"Image received")
f.close

client_socket.close()
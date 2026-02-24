### Client Script
## Import needed librabries
import socket       # communicate wirelessly
from ultralytics import YOLO        # YOLO object detection program to run the model
from time import perf_counter

start_time = perf_counter()

# Target IP of the Gopigo robot
targetIP = '10.10.10.10'
port = 6200

# Data size used when transfering image in bytes
datasize = 1024

# File to store the picture of the foward view
captureFile = r"C:\Users\s22br\Documents\gopigo\pics\capture.jpg"
timer = r"C:\Users\s22br\Documents\gopigo\time.txt"


# Parse user inputs
model_path = "../YOLO/my_model3/my_model.pt"
# Load the model into memory and get labemap
model = YOLO(model_path, task='detect')
labels = model.names

#'''
# Connect to the server
print(f"Starting the connection")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((targetIP, port))

while True:
    # Connect to the server fully
    print(f"Initiating the connection. Waiting for image")
    f = open(captureFile, 'wb')

    data = client_socket.recv(datasize)
    # Image is received from the server and kept as a file called "capture.jpg"
    while data:
        f.write(data)
        data = client_socket.recv(datasize)
    client_socket.shutdown(socket.SHUT_WR) # Signal no more data
    print(f"Image received")
    f.close()
    client_socket.close()
    # IMPORTANT: Conection closes on the server side due to indicate that the
        #file was transfered. We could not find a better way to go about it.
#'''

    # Run inference on frame
    results = model(captureFile)

    # Extract results
    detections = results[0].boxes

    # If the model doesn't find anything, the robot should just look around
    if not detections:
        direction = 'T'
        print(f"Target not found type 1, locating:")

    else:
        print(f"Target found")
        # Get bounding box confidence
        conf = detections[0].conf.item()

        if conf > 0.75:

            # Extract coordinates of the bounding box around the target
            xyxy_tensor = detections[0].xyxy.cpu() # Detections in Tensor format in CPU memory
            xyxy = xyxy_tensor.numpy().squeeze() # Convert tensors to Numpy array
            xmin, ymin, xmax, ymax = xyxy.astype(int) # Extract individual coordinates and convert to int
            print(xmin, ymin, xmax, ymax)
            height, width = results[0].orig_shape
            xcenter = (xmax - xmin)/2 + xmin
            ycenter = (ymax - ymin)/2 + ymin
            print(xcenter, ycenter)

            if ycenter > 300:
                direction = 'D'
            elif xcenter > width/2 + 200:
                direction = 'R'
            elif xcenter < width/2 - 200:
                direction = 'L'
            else:
                direction = 'S'
        else:
            direction = 'T'
            print(f"Target not found type 2, locating:")
        
    print(direction)

    # Connect again
    print(f"Starting new connection")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((targetIP, port))

    # Send instructions to server
    client_socket.send(direction.encode())
    #client_socket.close()

    if direction == 'D':
        client_socket.close()
        end_time = perf_counter()
        break

end_time = perf_counter()
duration_ms = (end_time - start_time) * 1000
print(f"Duration: {duration_ms:.6f} ms")
with open(timer, 'w') as file:
    file.write(str(duration_ms) + "ms" + '\n')


## 
## python yolo_detect.py --model my_model.pt capture.jpg

#client_socket.close()
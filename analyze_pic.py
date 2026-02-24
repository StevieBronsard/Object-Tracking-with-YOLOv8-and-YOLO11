import cv2
from ultralytics import YOLO

captureFile = r"C:\Users\s22br\Documents\gopigo\pics\capture.jpg"

# Parse user inputs
model_path = "../YOLO/my_model2/my_model.pt"
# Load the model into memory and get labemap
model = YOLO(model_path, task='detect')
labels = model.names

filename = r"C:\Users\s22br\Documents\gopigo\pics\test.png"

# Run inference on frame
results = model(captureFile)
results[0].save(filename)

# Extract results
#detections = results[0].boxes
#print(detections)

#cv2.imwrite(r"C:\Users\s22br\Documents\gopigo\pics\test.png", detections)

#captureFile2 = r"C:\Users\s22br\Documents\gopigo\pics\capture2.jpg"


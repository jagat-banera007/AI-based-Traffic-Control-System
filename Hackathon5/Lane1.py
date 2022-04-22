# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 19:43:30 2022

@author: JAGAT
"""
import cv2
import csv
import numpy as np
import sys
import multiprocessing
sys.path.insert(0, r'C:\Users\JAGAT\Downloads\vehicle-detection-classification-opencv\coco.names')
from utils.module import EuclideanDistTracker
from utils.vehicle_counter import count_vehicle
from utils.vehicle_counter import up_line_position
from utils.vehicle_counter import middle_line_position
from utils.vehicle_counter import down_line_position
from utils.vehicle_counter import up_list
from utils.vehicle_counter import down_list
#from utils.Dynamic_switch import switch_signal
from utils.Dynamic_switch import avg_signal_oc_time
from utils.traffic_lights1 import driver1

TimeLane = []
Lane = [] 
# Initialize Tracker
tracker = EuclideanDistTracker()

# Initialize the videocapture object
#cap = cv2.VideoCapture(r'C:\Users\JAGAT\Downloads\video5.mp4')
input_size = 320

# Detection confidence threshold
confThreshold =0.2
nmsThreshold= 0.2

font_color = (0, 0, 255)
font_size = 0.5
font_thickness = 2




# Store Coco Names in a list

classesFile = "C:\\Users\\JAGAT\\Desktop\\demo.txt"

classNames = open(classesFile).read().strip().split('\n')
print(classNames)
print(len(classNames))

# class index for our required detection classes
required_class_index = [2, 3, 5, 7]

detected_classNames = []

## Model Files
modelConfiguration = 'C:\\Users\\JAGAT\\Downloads\\vehicle-detection-classification-opencv\\yolov3-320.cfg'
modelWeigheights = 'C:\\Users\\JAGAT\\Downloads\\vehicle-detection-classification-opencv\\yolov3.weights'

# configure the network model
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeigheights)

# Configure the network backend

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Define random colour for each class
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classNames), 3), dtype='uint8')




# Function for finding the detected objects from the network output
def postProcess(outputs,img):
    global detected_classNames 
    height, width = img.shape[:2]
    boxes = []
    classIds = []
    confidence_scores = []
    detection = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if classId in required_class_index:
                if confidence > confThreshold:
                    # print(classId)
                    w,h = int(det[2]*width) , int(det[3]*height)
                    x,y = int((det[0]*width)-w/2) , int((det[1]*height)-h/2)
                    boxes.append([x,y,w,h])
                    classIds.append(classId)
                    confidence_scores.append(float(confidence))

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, confThreshold, nmsThreshold)
    # print(classIds)
    if len(indices) > 0 :
     for i in indices.flatten():
        x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
        # print(x,y,w,h)

        color = [int(c) for c in colors[classIds[i]]]
        name = classNames[classIds[i]]
        detected_classNames.append(name)
        # Draw classname and confidence score 
        cv2.putText(img,f'{name.upper()} {int(confidence_scores[i]*100)}%',
                  (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Draw bounding rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
        detection.append([x, y, w, h, required_class_index.index(classIds[i])])

    # Update the tracker for each object
    boxes_ids = tracker.update(detection)
    for box_id in boxes_ids:
        count_vehicle(box_id, img)


def realTime(param):
    cap = cv2.VideoCapture(param)
    cap.set(cv2.CAP_PROP_FPS, int(25))
    while True:
        
        success, img = cap.read()
        img = cv2.resize(img,(0,0),None,0.5,0.5)
        ih, iw, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)

        
        net.setInput(blob)
        layersNames = net.getLayerNames()
        outputNames = [(layersNames[i - 1]) for i in net.getUnconnectedOutLayers()]
        
        outputs = net.forward(outputNames)
    
        
        postProcess(outputs,img)

        

        cv2.line(img, (0, middle_line_position), (iw, middle_line_position), (255, 0, 255), 2)
        cv2.line(img, (0, up_line_position), (iw, up_line_position), (0, 0, 255), 2)
        cv2.line(img, (0, down_line_position), (iw, down_line_position), (0, 0, 255), 2)

    
        #cv2.putText(img, "Up", (110, 20), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(img, "Count", (160, 20), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(img, "Car:             "+ str(down_list[0]), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(img, "Motorbike:       "+ str(down_list[1]), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(img, "Bus:             "+ str(down_list[2]), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
        cv2.putText(img, "Truck:           "+ str(down_list[3]), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

        # Show the frames
        img = cv2.resize(img, (1280, 720)) 
        cv2.imshow('Output', img)
        
        
        
        if cv2.waitKey(1) == ord('q'):
            break
    Lane.append(sum(down_list))
   
    # Write the vehicle counting information in a file and save it
    with open(r"C:\Users\JAGAT\Documents\data.csv", 'w') as f1:
        cwriter = csv.writer(f1)
        cwriter.writerow(['Direction', 'car', 'motorbike', 'bus', 'truck'])
        up_list.insert(0, "Up")
        down_list.insert(0, "Down")
        cwriter.writerow(up_list)
        cwriter.writerow(down_list)
    down_list[:] = [0]*4
    up_list[:] = [0]*4
    f1.close()
    # print("Data saved at 'data.csv'")
    # Finally realese the capture object and destroy all active windows
    cap.release()
    cv2.destroyAllWindows()


'''image_file = 'C:\\Users\\JAGAT\\Downloads\\car.png'
def from_static_image(image):
    img = cv2.imread(image)

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)

    # Set the input of the network
    net.setInput(blob)
    layersNames = net.getLayerNames()
    outputNames = [(layersNames[i - 1]) for i in net.getUnconnectedOutLayers()]
    # Feed data to the network
    outputs = net.forward(outputNames)

    # Find the objects from the network output
    postProcess(outputs,img)

    # count the frequency of detected classes
    frequency = collections.Counter(detected_classNames)
    print(frequency)
    # Draw counting texts in the frame
    cv2.putText(img, "Car:        "+str(frequency['car']), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Motorbike:  "+str(frequency['motorbike']), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Bus:        "+str(frequency['bus']), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
    cv2.putText(img, "Truck:      "+str(frequency['truck']), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)


    cv2.imshow("image", img)

    cv2.waitKey(0)

    # save the data to a csv file
    with open("static-data.csv", 'a') as f1:
        cwriter = csv.writer(f1)
        cwriter.writerow([image, frequency['car'], frequency['motorbike'], frequency['bus'], frequency['truck']])
    f1.close()
'''
'''class camThread(threading.Thread):
    def __init__(self, video_path):
        threading.Thread.__init__(self)
        self.video_path = video_path


    def run(self):
        print("Starting " + self.video_path)
        realTime(self.video_path)
        '''

if __name__ == '__main__':
    files = ['C:\\Users\\JAGAT\\Downloads\\video5.mp4','C:\\Users\\JAGAT\\Downloads\\video2.mp4','C:\\Users\\JAGAT\Downloads\\video9.mp4','C:\\Users\\JAGAT\Downloads\\video11.mp4']
    for i in files :
       realTime(i)
    for x in range(len(Lane)):
      print (Lane[x])
    
    denser_lane = Lane.index(max(Lane)) + 1 
    dense_Lane = Lane[denser_lane-1]
    print (dense_Lane)
    seconds = avg_signal_oc_time(dense_Lane)
    print(seconds)
    for i in range(0,4):
        TimeLane.append(avg_signal_oc_time(Lane[i]))
    
    #switch_signal(denser_lane, seconds)
    driver1(seconds,TimeLane)
    #from_static_image(image_file)
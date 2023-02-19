'''
Code for detecting and localizing objects belonging to 3 classes of the MS COCO dataset using YOLO V4.
The 6 classes are : chair, table and person

References:
https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects
https://henryyu-98599.medium.com/train-yolov4-with-specific-categories-of-images-in-ms-coco-dataset-6937cac75bc1
https://lindevs.com/yolov4-object-detection-using-opencv

'''

# Import
import cv2
import numpy as np
import time


# Read class names
# with open('coco.names', 'r') as f: # Entire COCO Dataset
with open('obj_motion.names', 'r') as f: # 3 classes: chair, table and person
    classes = f.read().splitlines()
    # print(type(classes))


# Load the YOLO V4 Model with the config file modified for 3 classes and the weights file obtained after training
# Note : The weights files are not in the repo
# net = cv2.dnn.readNetFromDarknet("yolov4.cfg", "yolov4.weights") # pre-trained on entire MS COCO Dataset
net = cv2.dnn.readNetFromDarknet("yolo-obj_motion.cfg", "yolo-obj_motion.weights") # trained for 3 classes: chair, table and person
# print(net)


# CUDA Support (OpenCV needs to be built from source with CUDA Support)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
model = cv2.dnn_DetectionModel(net)
model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)


# Select Camera Source
cam = cv2.VideoCapture(0)   ## 0 - default webcam


# Detection and Bounding boxes
while True:
    ret,img = cam.read()
    
    classIds, scores, boxes = model.detect(img, confThreshold=0.6, nmsThreshold=0.4)

    for (classId, score, box) in zip(classIds, scores, boxes):
        # print("box", box)
        cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                  color=(0, 255, 0), thickness=2)
        text = '%s: %.2f' % (classes[classId], score)
        cv2.putText(img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
                color=(0, 255, 0), thickness=2)

    cv2.imshow("Webcam",img)
    #print(ret,img)
    if cv2.waitKey(1)  == 13:     ### 13 is the ASCII code for enter
        break
cam.release()
cv2.destroyAllWindows()
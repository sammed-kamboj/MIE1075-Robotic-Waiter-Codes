'''
Code for detecting and localizing objects belonging to 6 classes of the MS COCO dataset using YOLO V4.
The 6 classes are : spoon, fork, knife, wine glass, cup, bowl


References:
https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects
https://henryyu-98599.medium.com/train-yolov4-with-specific-categories-of-images-in-ms-coco-dataset-6937cac75bc1
https://lindevs.com/yolov4-object-detection-using-opencv

'''


# Import
import cv2
import numpy as np


# Load Test Image
img = cv2.imread("test2.jpg")


# Read class names
# with open('coco.names', 'r') as f: # Entire COCO Dataset
# with open('obj_motion.names', 'r') as f: # 3 classes: chair, table and person
with open('obj_tableware.names', 'r') as f: # 6 classes : spoon, fork, knife, wine glass, cup, bowl
    classes = f.read().splitlines()


# Load the YOLO V4 Model
# Note : The weights files are not in the repo
# net = cv2.dnn.readNetFromDarknet("yolov4.cfg", "yolov4.weights") # pre-trained on entire MS COCO Dataset
# net = cv2.dnn.readNetFromDarknet("yolo-obj_motion.cfg", "yolo-obj_motion.weights") # trained for 3 classes: chair, table and person
net = cv2.dnn.readNetFromDarknet("yolo-obj_tableware.cfg", "yolo-obj_tableware.weights") # trained for 6 classes : spoon, fork, knife, wine glass, cup, bowl
# print(net)
model = cv2.dnn_DetectionModel(net)
model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)


# Detection and Bounding boxes
classIds, scores, boxes = model.detect(img, confThreshold=0.4, nmsThreshold=0.4)
for (classId, score, box) in zip(classIds, scores, boxes):
    cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                  color=(0, 255, 0), thickness=1)
    # print("box ", box)
    text = '%s: %.2f' % (classes[classId], score)
    # print(text)
    cv2.putText(img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                color=(0, 255, 0), thickness=1) #2
cv2.imshow('YOLO', img)
cv2.imwrite("Result.jpg", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
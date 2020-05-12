import cv2
import numpy as np
class detector:
    def __init__(self):
        self.net = cv2.dnn.readNet("yolov3-tiny-obj_9000327.weights", "yolov3-tiny-obj326.cfg")
        self.classes = []
        with open("obj.names.txt", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def detect(self,img):
        height, width, channels = img.shape
        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.003, (416, 416), (0, 0, 0), True, crop=False)

        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        class_ids = []
        confidences = []
        boxes = []
        centers = []
        for out in outs:
            for detection in out:

                scores = detection[5:]

                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.01:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    centers.append([center_x, center_y])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        return boxes,confidences,centers,self.colors

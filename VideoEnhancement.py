import cv2
import retinex
import json

with open('config.json', 'r') as f:
    config = json.load(f)

def enhanceVideo(frame,resize):

 if(resize):
     frame = cv2.resize(frame, (640, 352))

 enhancedFrame = retinex.automatedMSRCR(frame,config['sigma_list'])

 return enhancedFrame






import cv2
import retinex

def enhanceVideo(frame,resize):

 if(resize):
     frame = cv2.resize(frame, (640, 352))

 enhancedFrame = retinex.automatedMSRCR(frame)

 return enhancedFrame






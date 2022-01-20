import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pyzbar.wrapper import ZBarSymbol


# Connect via USB
'''
To connect via USB, select transfer photos, enable usb debugging in developer mode, open Droid cam and Droid
Client, refresh, connect to in Droid Client then run this code.
'''
# Set camera
cap = cv2.VideoCapture(1)

# Set camera dims
cap.set(3,640)
cap.set(4,480)

# Decode barcode in images
while True:
    success,img = cap.read()
    for barcode in decode(img):
        
        myData = barcode.data.decode('utf-8')
        print(myData)


    cv2.imshow('Result',img)
    # use 1 for streaming
    cv2.waitKey(1)




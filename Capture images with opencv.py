import cv2

# Connect to mobile camera via wifi
cap = cv2.VideoCapture('http://192.168.1.42:4747/video')

# Set camera dims
cap.set(3,960)
cap.set(4,720)

# Capturing image on pressing spacebar
while(True):
    ret,frame = cap.read()
    cv2.imshow('img1',frame) #display the captured image
    if cv2.waitKey(1) & 0xFF == ord(' '): #save on pressing spacebar 
        cv2.imwrite('captures/ c1.png',frame)
        cv2.destroyAllWindows()
        break

cap.release()
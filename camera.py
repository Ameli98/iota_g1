import cv2

# Open camera and qrcode detector
cap = cv2.VideoCapture(0)
qrcode = cv2.QRCodeDetector()

while(True):
    # fetch an frame from camera
    ret, frame = cap.read()

    # Show the frame
    cv2.imshow('frame', frame)

    # scan the frame for qrcode
    data, bbox, rectified = qrcode.detectAndDecode(frame)
    if bbox is not None:
       print(data)
       break

# release camera
cap.release()

# close all the cv2 windows
cv2.destroyAllWindows()
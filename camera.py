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

    # press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()
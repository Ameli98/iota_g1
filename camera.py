import cv2

# Open camera and qrcode detector
cap = cv2.VideoCapture(0)
qrcode = cv2.QRCodeDetector()

# open json file
output_file = open("data.json", "w")

while(True):
    # fetch an frame from camera
    ret, frame = cap.read()

    # Show the frame
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    # scan the frame for qrcode
    data, bbox, rectified = qrcode.detectAndDecode(frame)
    if data != "":
        print(data, file=output_file)
        break

    # press 'q' to exit
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()
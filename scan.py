import cv2
import json

def scan(user:str):
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
            data = data.replace("\'", "\"")
            data = json.loads(data)
            data["user"] = user
            json.dump(data, output_file)
            break

        # press 'q' to exit
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # release the camera
    cap.release()

    # close all windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan("Lux")
import cv2
import json
import datetime
import os
from dotenv import load_dotenv

def scan(user:str):
    # Open camera and qrcode detector
    cap = cv2.VideoCapture(0)
    qrcode = cv2.QRCodeDetector()

    # open json file
    with open("data.json", "w") as output_file:

        while(True):
            # fetch an frame from camera
            ret, frame = cap.read()

            # Show the frame
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
            # scan the frame for qrcode
            data, bbox, rectified = qrcode.detectAndDecode(frame)
            # write the qrcode message into data.json
            if data != "":
                data = data.replace("\'", "\"")
                data = json.loads(data)

                data["user"] = user
                data["date"] = str(datetime.date.today())
                data["due"] = str(datetime.date.today() + datetime.timedelta(days=60))
                load_dotenv()
                place = os.getenv("PLACE")
                data["place"] = place

                json.dump(data, output_file)
                print("Success! Process recorded.")
                break

            # press 'q' to exit
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        # release the camera
        cap.release()

        # close all windows
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # scan("Lux")
    print(datetime.date.today() + datetime.timedelta(days=60))
import cv2
import json
import datetime
import os
from dotenv import load_dotenv
from search import search, synchronize

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

                load_dotenv()
                place = os.getenv("PLACE")
                data["place"] = place

                try:
                    last_data = search(data["name"])
                except FileNotFoundError:
                    synchronize()
                try:
                    if last_data["status"] == "borrow":
                        data["status"] = "return"
                    else:
                        data["status"] = "borrow"
                except KeyError:
                    print("error")
                    data["status"] = "borrow"
                
                if data["status"] == "borrow":
                    data["date"] = str(datetime.date.today())
                    data["due"] = str(datetime.date.today() + datetime.timedelta(days=60))
                else:
                    data["date"] = str(datetime.date.today())
                    data["due"] = last_data["due"]

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
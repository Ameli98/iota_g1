import json
import argparse
from dotenv import load_dotenv
import subprocess, os, sys
import iota_client
from upload import synchronize


def search(name:str):
    # synchronize and load message_id.json
    synchronize()

    # Load json
    with open("message_id.json", "r") as m:
        try:
            id_set = json.load(m)
        except json.decoder.JSONDecodeError:
            id_set = {}

    try:
        id = id_set[name]
    except KeyError:
        print("No such book exists")
        return None

    # Get message from iota
    client = iota_client.Client()
    message = client.get_message_data(id)
    ascii_data = message["payload"]["indexation"][0]["data"]
    data = ""
    for char in ascii_data:
        data += chr(char)
    data = data.replace("'", "\"")
    data = json.loads(data)

    return data

if __name__ == "__main__":
    # Load argument
    parser = argparse.ArgumentParser()
    parser.add_argument("BookName", type=str, help="the book you want to find")
    args = parser.parse_args()

    # synchronize and load message_id.json
    load_dotenv()
    destination = os.getenv("DESTINATION")
    subprocess.run(["scp", destination, "message_id.json"])

    # Load json
    with open("message_id.json", "r") as m:
        try:
            id_set = json.load(m)
        except json.decoder.JSONDecodeError:
            id_set = {}

    try:
        id = id_set[args.BookName]
    except KeyError:
        print("No such book exists")
        os._exit(1)

    # Get message from iota
    client = iota_client.Client()
    message = client.get_message_data(id)
    ascii_data = message["payload"]["indexation"][0]["data"]
    data = ""
    for char in ascii_data:
        data += chr(char)
    data = data.replace("'", "\"")
    data = json.loads(data)

    # print data
    print("Name: " + data["name"])
    print("Price: " + data["price"])
    if data["status"] == "borrow":
        print("Status: Last borrowed from " + data["place"])
    else:
        print("Status: in " + data["place"])

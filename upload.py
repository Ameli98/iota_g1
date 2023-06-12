import iota_client
import json
import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv


def synchronize():
    load_dotenv()
    destination = os.getenv("DESTINATION")
    subprocess.run(["scp", destination, "message_id.json"])
    return destination


def upload():
    client = iota_client.Client()

    with open("data.json", "r") as f:
        data = json.load(f)
        name = data["name"]
        status = data["status"]
        due = datetime.strptime(data["due"], "%Y-%m-%d")
        if status == "return":
            if due < datetime.today():
                print(
                    f"Overdued!! you should have return {name} before {str(due)}.")
            else:
                print("Return successfully.")
        else:
            print(f"Operation success. Please return {name} before {str(due)}")

    message = client.message(
        index="some_data_index", data=str(data).encode("utf8")
    )
    id = message["message_id"]

    # Synchronize message_id.json from the database
    destination = synchronize()

    # Record message_id in message_id.json
    with open("message_id.json", "r") as m:
        try:
            id_set = json.load(m)
        except json.decoder.JSONDecodeError:
            id_set = {}
        id_set[name] = id

    with open("message_id.json", "w") as m:
        json.dump(id_set, m)

    # Update the latest message_id.json to the database
    subprocess.run(["scp", "message_id.json", destination])


if __name__ == "__main__":
    upload()

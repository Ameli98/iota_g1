import iota_client, json, subprocess, os
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
    # encoding utf string into list of bytes
    # data = {
    #     "name": "Bible",
    #     "status": "borrow",        # borrow / return
    #     "user": "Amelia Huang",
    #     "from": "NTU_liabrary",
    #     "date": "1/1/2023",
    #     "due": "3/1/2023"
    #     }
    # data = "some utf based data".encode("utf8")

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
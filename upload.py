import iota_client
from pprint import pprint


client = iota_client.Client()

f = open("data.json", "r")

# encoding utf string into list of bytes
data = f.readline()
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
pprint(message)
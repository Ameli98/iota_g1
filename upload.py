import iota_client
from pprint import pprint
import json


client = iota_client.Client()

# encoding utf string into list of bytes
data = {
    'name': 'Bible',
    'status': 'borrow',        # borrow / return
    'user': 'Amelia Huang',
    'from': 'NTU_liabrary',
    'date': '1/1/2023',
    'due': '3/1/2023',
    }
# data = "some utf based data".encode("utf8")

message = client.message(
    index="some_data_indey", data=str(data).encode("utf8")
)
pprint(message)
import iota_wallet as iw
import json
import os
from dotenv import load_dotenv
from pprint import pprint

# Load the env variables
load_dotenv()
# Get the stronghold password
STRONGHOLD_PASSWORD = os.getenv('SH_PASSWORD')
# This example checks the account balance.
account_manager = iw.AccountManager(
    storage_path="./library_database"
)
account_manager.set_stronghold_password(STRONGHOLD_PASSWORD)


def pay(username: str):
    # get a specific instance of some account
    account = account_manager.get_account(username)
    print(f'Account: {account.alias()} selected')

    # Always sync before doing anything with the account
    print('Syncing...')
    synced = account.sync().execute()

    # get total balance for the account
    pprint(f"Account balance: {account.balance()['available']}")

    with open("data.json", "r") as f:
        data = json.load(f)
        price = int(data["price"])

    # TODO: Replace with the address of your choice!
    transfer = iw.Transfer(
        amount=price*1000000,
        address="atoi1qzgenqh9nkn0tdd6fryn9lugsvesvxavdsgzr4ay5x2axgf32zxsqvj4fqa",
        remainder_value_strategy='ReuseAddress'
    )

    # Propogate the Transfer to Tangle
    # and get a response from the Tangle
    print("Payment process starts, please wait.")
    node_response = account.transfer(transfer)
    # pprint(node_response)

    print("Finish payment!")

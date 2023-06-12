import iota_wallet as iw
import json
import os
from dotenv import load_dotenv

# Load the env variables｀
load_dotenv()
# Get the stronghold password
STRONGHOLD_PASSWORD = os.getenv('SH_PASSWORD')
# This example checks the account balance.
account_manager = iw.AccountManager(
    storage_path="./library_database"
)
account_manager.set_stronghold_password(STRONGHOLD_PASSWORD)


def pay(username: str):
    print("--------- Payment Process Start -------------")
    # get a specific instance of some account
    account = account_manager.get_account(username)
    print(f'Account: {account.alias()} selected')

    # Always sync before doing anything with the account
    print('Syncing...')
    synced = account.sync().execute()

    # get total balance for the account
    print(f"Account balance: {account.balance()['available']/1000000} dollar")

    with open("data.json", "r") as f:
        data = json.load(f)
        price = int(data["price"])
    print(f"The rental fee of this book is {price} dollar.")

    if account.balance()['available'] < price*1000000:
        print("Your account balance isn't enough, payment failed.")
        return False

    while True:
        confirm = input(
            "Your account balance is enough, are you sure to rent this book? (yes/no) ")

        yes_choices = ['yes', 'y']
        no_choices = ['no', 'n']

        if confirm.lower() in no_choices:
            print("Stop rental process.")

            return False
        elif confirm.lower() in yes_choices:
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
            print(
                f"Finish payment! Account balance: {account.balance()['available']}")
            print("--------- Payment Process End --------------")

            return True

        else:
            print("Please type yes or no.")

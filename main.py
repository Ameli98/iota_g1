from scan import scan
from upload import upload
from pay import pay
import os
from getpass import getpass
import argparse
import json
import iota_wallet as iw
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


def main(username=None, overdue=False):
    scan(username, overdue)
    if pay(username):
        upload()


if __name__ == "__main__":
    # option build
    parser = argparse.ArgumentParser()
    parser.add_argument("-un", "--user_name", type=str, nargs="?", help="your username")
    parser.add_argument("-bn", "--book_number", nargs="?", type=int,
                        default=1, help="number of books you want to borrow or return")
    parser.add_argument("-od", "--overdue_demo",
                        action="store_true", help="Demo of overdueing")

    args = parser.parse_args()

    # load right password from database
    with open("account.json", "r") as acc:
        account_set = json.load(acc)
    if not args.user_name:
        address = input("Your address: ")
        for user in account_set.keys():
            account = account_manager.get_account(user)

            address_list = []
            for i in range(4):
                address_list.append(account.addresses()[i]['address']['inner'])

            if address in address_list:
                # get a specific instance of some account
                account = account_manager.get_account(user)
                print(f'User {account.alias()} login')
                user_exist = True
                username = user
                break
        if not user_exist:
            print("User is not exist. Process terminated.")
            os._exit(1)
    else:
        username = args.user_name
        try:
            right_password = account_set[username]
            user_exist = True
        except KeyError:
            print("No such user exists, session terminated.")
            os._exit(1)

    # login
    attempt = 0
    while True:
        password = getpass()
        attempt += 1
        if password == account_set[username]:
            print("User recognized, logging...")
            for i in range(args.book_number):
                main(username, args.overdue_demo)
            break
        elif attempt >= 3:
            print("Too many attempts, session terminated.")
            os._exit(1)
        else:
            print("Wrong password, access denied.")
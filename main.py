from scan import scan
from upload import upload

import os
from getpass import getpass
import argparse, json
from pay import pay

# the borrow/lend process
def main(username):
    scan(username)
    upload()
    pay(username)
    

if __name__ == "__main__":
    # option build
    parser = argparse.ArgumentParser()
    parser.add_argument("user_name", type=str, help="your username")
    parser.add_argument("-bn", "--book_number", nargs="?", type=int, default=1, help="number of books you want to borrow or return")
    args = parser.parse_args()

    # load right password from database
    with open("account.json", "r") as acc:
        account_set = json.load(acc)
    username = args.user_name
    try:
        right_password = account_set[username]
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
                main(username)
            break
        elif attempt >= 3:
            print("Too many attempts, session terminated.")
            os._exit(1)
        else:
            print("Wrong password, access denied.")


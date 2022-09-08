# Write your code here
import random
import sqlite3

'''
class Card:
    def __init__(self):
        random.seed(random.random())
        self.card_number = "400000{}{}".format(random.randint(10 ** 8, 10 ** 9 - 1), random.randint(0, 9))
        self.pin = "".join([str(random.randint(0, 9)) for _ in range(4)])
        self.balance = 0

    def get_card_number(self):
        return self.card_number

    def get_pin(self):
        return self.pin

    def get_balance(self):
        return self.balance
'''


def luhn_algorithm(unchecked):
    checksum = 0
    for i in range(len(unchecked)):
        if i % 2 == 0:
            if int(unchecked[i]) * 2 > 9:
                checksum += int(unchecked[i]) * 2 - 9
            else:
                checksum += int(unchecked[i]) * 2
        else:
            checksum += int(unchecked[i])
    return checksum % 10


def gen_card_number():
    random.seed(random.random())
    bin_number = str(400000)
    cai_number = str(random.randint(10 ** 8, 10 ** 9 - 1))
    checksum = str((10 - luhn_algorithm(bin_number + cai_number)) % 10)
    card_number = bin_number + cai_number + checksum
    return card_number


def gen_pin():
    random.seed(random.random())
    pin = "".join([str(random.randint(0, 9)) for _ in range(4)])
    return pin


def is_empty():
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    if cur.fetchall() is None:
        return True
    else:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cur.fetchall())
        return False


def implement_table():
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS card (
    id INTEGER PRIMARY KEY,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    );""")
    conn.commit()


def add_card(card_number, pin):
    cur = conn.cursor()
    cur.execute("""INSERT INTO card (number, pin)
    VALUES ('{}', '{}');""".format(card_number, pin))
    conn.commit()


def get_card(card_number):
    cur = conn.cursor()
    cur.execute("""SELECT
    number,
    pin,
    balance
    FROM card
    WHERE number = '{}';
    """.format(card_number))
    data = cur.fetchone()
    if data is None:
        return None
    else:
        card = {'card_number': str(data[0]), 'pin': str(data[1]), 'balance': int(data[2])}
        return card


def update_card(this_card):
    cur = conn.cursor()
    cur.execute("""UPDATE card
    SET balance = {}
    WHERE number = '{}';""".format(this_card.get('balance'), this_card.get('card_number')))
    conn.commit()


def delete_card(this_card):
    cur = conn.cursor()
    cur.execute("""DELETE FROM card
    WHERE number = {}""".format(this_card.get('card_number')))
    conn.commit()


global conn
conn = sqlite3.connect('card.s3db')
implement_table()
main_menu = """1. Create an account
2. Log into account
0. Exit"""
log_menu = """1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit"""
menu_pool = {"main": main_menu, "log": log_menu}
menu_state = "main"
global current_card
while menu_state != "exit":
    print(menu_pool.get(menu_state))
    choose = input()
    if menu_state == "main":
        if choose == "1":
            card_number = gen_card_number()
            pin = gen_pin()
            balance = 0
            print("\nYour card has been created")
            print("Your card number:\n{}".format(card_number))
            print("Your card PIN:\n{}\n".format(pin))
            add_card(card_number, pin)
        elif choose == "2":
            card_number = str(input("\nEnter your card number:\n"))
            pin = str(input("Enter your card PIN:\n"))
            card = get_card(card_number)
            if card is not None and card.get("pin") == pin:
                print("\nYou successfully logged in!\n")
                current_card = card
                menu_state = "log"
            else:
                print("\nWrong card number or PIN!")
        elif choose == "0":
            print("\nBye!")
            menu_state = "exit"
        else:
            print("\nUnknown command")
    elif menu_state == "log":
        if choose == "1":
            print("\nBalance: {}".format(current_card.get("balance")))
        elif choose == "2":
            income = int(input("\nEnter income:\n"))
            income += current_card.get('balance')
            current_card.update(balance=income)
            update_card(current_card)
            print("Income was added!\n")
        elif choose == "3":
            print("\nTransfer")
            receiver_card_number = input("Enter card number:\n")
            if luhn_algorithm(receiver_card_number) == 0:
                if get_card(receiver_card_number) is None:
                    print("Such a card does not exist.")
                else:
                    outcome = int(input("Enter how much money you want to transfer:\n"))
                    if outcome > current_card.get('balance'):
                        print("Not enough money!")
                    else:
                        balance = current_card.get('balance') - outcome
                        current_card.update(balance=balance)
                        update_card(current_card)
                        receiver_card = get_card(receiver_card_number)
                        balance = receiver_card.get('balance') + outcome
                        receiver_card.update(balance=balance)
                        update_card(receiver_card)
                        print("Success!")
            else:
                print("Probably you made a mistake in the card number. Please try again!")
        elif choose == "4":
            delete_card(current_card)
            print("\nThe account has been closed!\n")
            menu_state = "main"
        elif choose == "5":
            print("\nYou have successfully logged out!\n")
            menu_state = "main"
        elif choose == "0":
            print("\nBye!")
            menu_state = "exit"
conn.close()

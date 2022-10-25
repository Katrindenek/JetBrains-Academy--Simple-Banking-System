# Write your code here
import random
import string
import math
import sqlite3

DIGITS = string.digits


# The class is used to generate a bank account
class BankAccount:
    IIN = '400000'

    def __init__(self):
        account_number = self._generate_account()
        self.pin = self._generate_pin()
        self.card_number = self._generate_card_number(account_number)

    @classmethod  # Luhn algorithm to get a checksum for a card number validation
    def generate_checksum(cls, account_number):
        card_number_wo_checksum = cls.IIN + account_number
        split_number = list(map(int, list(card_number_wo_checksum)))
        even_pos_mult_by_2 = [split_number[i] * 2 if i % 2 == 0 else split_number[i]
                              for i in range(len(split_number))]
        sub_9_if_over_9 = [n - 9 if n > 9 else n for n in even_pos_mult_by_2]
        sum_of_nums = sum(sub_9_if_over_9)
        total_num = math.ceil(sum_of_nums / 10) * 10
        return str(total_num - sum_of_nums)

    def _generate_card_number(self, account_number):
        checksum = BankAccount.generate_checksum(account_number)
        return self.IIN + account_number + checksum

    def _generate_account(self):
        return ''.join(random.sample(DIGITS, 9))

    def _generate_pin(self):
        return ''.join(random.sample(DIGITS, 4))


class BankApplication:
    database_name = "card.s3db"

    def __init__(self):
        self.conn = sqlite3.connect(self.database_name)
        self.cur = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0)
        """
        self.cur.execute(create_table_query)
        self.conn.commit()

    def create_account(self):
        """
        Creates a new bank account and adds to the database.

        :return: The ID of created bank account in the database or None if failed.
        """
        while True:
            new_account = BankAccount()
            check_exists_query = f"""
                SELECT * FROM card
                WHERE number = {new_account.card_number}
            """
            self.cur.execute(check_exists_query)

            if not self.cur.fetchone():
                create_account_query = f"""
                    INSERT INTO card (number, pin)
                    VALUES ({new_account.card_number}, {new_account.pin})
                """
                self.cur.execute(create_account_query)
                self.conn.commit()
                return self.log_into_account(new_account.card_number, new_account.pin)
        return None

    def log_into_account(self, card_number, pin):
        """
        Finds the ID of the given card to log in.

        :param card_number: The 16-digits string of user's card number.
        :param pin: The 4-digits string of user's pin code.
        :return: The ID of the user's account or None if failed.
        """
        select_account_query = f"""
            SELECT id FROM card
            WHERE number = {card_number} AND pin = {pin}
        """
        self.cur.execute(select_account_query)
        result_tuple = self.cur.fetchone()
        return result_tuple[0] if result_tuple else None

    def check_balance(self, account_id):
        check_balance_query = f"""
            SELECT balance FROM card
            WHERE id = {account_id}
        """
        self.cur.execute(check_balance_query)
        return self.cur.fetchone()[0]

    def add_income(self, account_id, income):
        update_balance_query = f"""
            UPDATE card
            SET balance = balance + {income}
            WHERE id = {account_id}
        """
        self.cur.execute(update_balance_query)
        self.conn.commit()

    def do_transaction(self, account_id, to_card_number, amount):
        """
        Performs a money transfer from the user's account to the given card.

        :param account_id: The ID of the user's account in the database.
        :param to_card_number: The number of the card to transfer money to.
        :param amount: The amount of money.
        :return: True if the transaction was successful, or False if it failed.
        """
        take_from_account_query = f"""
            UPDATE card
            SET balance = balance - {amount}
            WHERE id = {account_id}
        """
        add_to_card_number_query = f"""
            UPDATE card
            SET balance = balance + {amount}
            WHERE number = {to_card_number}
        """
        transaction_result = False
        self.cur.execute("begin")
        try:
            self.cur.execute(take_from_account_query)
            self.cur.execute(add_to_card_number_query)
            self.cur.execute("commit")
            transaction_result = True
        except self.conn.Error:
            self.cur.execute("rollback")

        return transaction_result

    def close_account(self, account_id):
        delete_account_query = f"""
            DELETE FROM card
            WHERE id = {account_id}
        """
        self.cur.execute(delete_account_query)
        self.conn.commit()

    def validate_checksum(self, card_number):
        """
        Checks if the card number is valid according to the Luhn algorithm.

        :param card_number: The 16-digits card number.
        :return: True if the card number is valid, or False otherwise.
        """
        if len(card_number) == 16:
            account_number = card_number[6:15]
            checksum = BankAccount.generate_checksum(account_number)
            return checksum == card_number[-1]
        return False

    def exists(self, card_number):
        select_account_query = f"""
            SELECT id FROM card
            WHERE number = {card_number}
        """
        self.cur.execute(select_account_query)
        result_id = self.cur.fetchone()
        return result_id[0] if result_id else None

    def print_card_info(self, account_id):
        select_card_info_query = f"""
            SELECT number, pin FROM card
            WHERE id = {account_id}
        """
        self.cur.execute(select_card_info_query)
        card_number, card_pin = self.cur.fetchone()
        print('Your card number:\n'
              '{}'.format(card_number))
        print('Your card PIN:\n'
              '{}'.format(card_pin))

    def print_menu(self, account_id):
        """
        Prints menu depending on whether the user is logged in or not.

        :param account_id: The ID of the logged in account or None.
        """
        if account_id:
            print("1. Balance\n"
                  "2. Add income\n"
                  "3. Do transfer\n"
                  "4. Close account\n"
                  "5. Log out\n"
                  "0. Exit")
        else:
            print("1. Create an account\n"
                  "2. Log into account\n"
                  "0. Exit")

    def user_choice(self, user_input, account_id):
        """
        Processes user's choice depending on whether the user is logged in or not.

        :param user_input: The digit that the user entered.
        :param account_id: The ID of the logged in account or None.
        :return: 0 if Exit, the account ID if the account stays logged in, None otherwise.
        """
        if user_input == '0':  # Exit
            self.conn.close()
            print('Bye!')
            return 0

        if account_id:  # Logged in
            if user_input == '1':  # Balance
                balance = self.check_balance(account_id)
                print(f"Balance: {balance}")
                return account_id
            elif user_input == '2':  # Add income
                print("Enter income:")
                income = int(input())
                self.add_income(account_id, income)
                print("Income was added!")
                return account_id
            elif user_input == '3':  # Do transfer
                print("Enter card number:")
                card_number = input()
                if not self.validate_checksum(card_number):
                    print("Probably you made a mistake in the card number. "
                          "Please try again!")
                elif not self.exists(card_number):
                    print("Such a card does not exist.")
                elif account_id == self.exists(card_number):
                    print("You can't transfer money to the same account!")
                else:
                    print("Enter how much money you want to transfer:")
                    transfer_money = int(input())
                    if self.check_balance(account_id) < transfer_money:
                        print("Not enough money!")
                    else:
                        result = self.do_transaction(account_id, card_number, transfer_money)
                        if result:
                            print("Success!")
                        else:
                            print("Transaction failed! Please try again!")
                return account_id
            elif user_input == '4':  # Close account
                self.close_account(account_id)
                print("The account has been closed!")
                return None
            elif user_input == '5':  # Log out
                print("You have successfully logged out!")
                return None
        else:  # Not logged in
            if user_input == '1':  # Create account
                account_id = self.create_account()
                if account_id:
                    print("Your card has been created")
                    self.print_card_info(account_id)
                return None

            elif user_input == '2':  # Log into account
                print("Enter your card number:")
                card_number = input()
                print("Enter your PIN:")
                pin = input()
                account_id = self.log_into_account(card_number, pin)
                if account_id:
                    print("You have successfully logged in!")
                else:
                    print("Wrong card number or PIN!")
                return account_id


if __name__ == '__main__':
    random.seed()
    logged_in_account = None
    app = BankApplication()
    while True:
        app.print_menu(logged_in_account)
        logged_in_account = app.user_choice(input(), logged_in_account)
        if logged_in_account == 0:
            break


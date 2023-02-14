# Bank Application
 
A bank application for creating a bank account, storing and managing account information in a SQLite database. The application also supports logging in, checking balance, adding income and doing transactions between bank accounts.

## Features
- Creating a new bank account with a 16-digits card number (using the Luhn algorithm) and 4-digits pin code.
- Storing the bank account information in a SQLite database.
- Logging into the account using card number and pin code.
- Checking the balance of the account.
- Adding income to the account.
- Doing transactions between bank accounts.

## Requirements
- Python 3.7 or higher
- SQLite3

## Usage
1. Run the `banking.py` file to start the application.
2. Choose an option from the menu:
    - Create an account: Get a generated card number and a pin code.
    - Log into account: Enter your card number and pin.
    - Exit: Exists the program.
3. When logged into account choose an option from the menu:
    - Balance: Check the balance in the account.
    - Add income: Add money to the account.
    - Do transfer: Transfer money to another account.
    - Close account: Close the bank account.
    - Log out: Log out from the account and return to the main menu.
    - Exit: Exists the program.

## Example
Start, create an account:
```commandline
1. Create an account
2. Log into account
0. Exit
> 1
Your card has been created
Your card number:
4000009321570866
Your card PIN:
8304
1. Create an account
2. Log into account
0. Exit
```

Log into the account:
```commandline
1. Create an account
2. Log into account
0. Exit
> 2
Enter your card number:
> 4000009321570866
Enter your PIN:
> 8304
You have successfully logged in!
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
```

Add money to the account and check the balance:
```commandline
> 2
Enter income:
> 100
Income was added!
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
> 1
Balance: 100
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
```

## Acknowledgement
The project is done as a part of [SQL with Python](https://hyperskill.org/projects/109?track=30) track by JetBrains Academy with Hyperskill. 
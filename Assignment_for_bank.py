# Name:Muhammad Bilal
# Data Analysis Batch: 317
# Scenario: "Cash Withdrawl"
# Assignment Number: 01

bank = input("enter a bank name: ")
# Business account for union consult
username = input("enter a account holder name: ")
password = input("enter a account password: ")

# Total Account Balance
Balance = 90009
Atmpin = int(input("enter a pin number: "))
withdrawl_amount = float(input("enter withdrawl amount: "))
if withdrawl_amount <= 0:
    print("invalid amount. ")
elif withdrawl_amount <= Balance:
    print("withdrawl successful. ")
else:
    print("insufficient funds. ")
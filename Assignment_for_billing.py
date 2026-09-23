# Name:Muhammad Bilal
# Data Analysis Batch: 317
# Scenario: "Bill Disscount As Per Ratting"
# Assignment Number: 01

# Branch Name
Branch = input("enter a branch name: ")
# Branch Code
Branch_code = int(input("enter a branch code :"))
# Total Bill
total_bill = float(input("enter total bill amount: "))
if total_bill <= 0:
    print("invalid amount. ")   

# customer rating
customer_rating = float(input("enter customer rating (1-5): "))
if customer_rating < 1 or customer_rating > 5:
    print("invalid rating. ")
elif customer_rating == 5:
    discount = total_bill * 0.20
    final_bill = total_bill - discount
    print("discount applied: ", discount)
    print("final bill amount: ", final_bill)
elif customer_rating == 4.5:
    discount = total_bill * 0.15
    final_bill = total_bill - discount
    print("discount applied: ", discount)
    print("final bill amount: ", final_bill)
elif customer_rating == 4:
    discount = total_bill * 0.10
    final_bill = total_bill - discount
    print("discount applied: ", discount)
    print("final bill amount: ", final_bill)
elif customer_rating == 3:
    discount = total_bill * 0.05
    final_bill = total_bill - discount
    print("discount applied: ", discount)
    print("final bill amount: ", final_bill)
elif customer_rating == 2:
    discount = total_bill * 0.02
    final_bill = total_bill - discount
    print("discount applied: ", discount)
    print("final bill amount: ", final_bill)
elif customer_rating == 1:
    discount = total_bill * 0.01
    final_bill = total_bill - discount
    print("discount applied: ", discount)
    print("final bill amount: ", final_bill)
else:
    print("no discount applied. ")
   
# Note :
NOte = int(input("Thaks for ratting "))
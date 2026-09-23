# Name : Muhammad Bilal Khan
# Scenario : Clothes Rental Store Management
# Data Analysis 
# Assignment : 3
# Date : 05/09/2026

from datetime import datetime, timedelta

# Store title
print("WELCOME TO THE STORE:")
print("Hermès")
print("www.hermes@gmail.com")
print("Contact: 021222111000")

# Client Details 
customer_name = input("Enter the client name: ").strip()
while not customer_name:
    print("Customer name cannot be empty.")
    customer_name = input("Enter the client name: ").strip()

# Rental Avalible Cloth list 
cloth_types = {
    1: ("Formal cloth", 33599),
    2: ("Casual cloth", 25000),
    3: ("Semi formal", 28990),
    4: ("Long coat", 20000),
    5: ("Short coat", 15000),
}

# Select The Cloth With Budget Price
print("\nAvailable clothes:")
for number, (cloth_name, price) in cloth_types.items():
    print(f"{number}. {cloth_name} - Rs. {price} per day")

# Customer Reffer To Esthatic Cloth Type 
while True:
    try:
        choice = int(input("Select a cloth type (1-5): "))
        if choice in cloth_types:
            break
        print("Please select a number from 1 to 5.")
    except ValueError:
        print("Please enter a valid number.")

# Client The Need To Rent Cloth A Few Days
while True:
    try:
        rental_days = int(input("Enter the number of rental days: "))
        if rental_days > 0:
            break
        print("Rental days must be greater than zero.")
    except ValueError:
        print("Please enter a whole number.")

# Store This Cloth Hand Over The Client And Start The Rent Day
while True:
    try:
        rental_start = datetime.strptime(
            input("Enter the rental start date (YYYY-MM-DD): "), "%Y-%m-%d"
        ).date()
        break
    except ValueError:
        print("Please use the date format YYYY-MM-DD.")

due_date = rental_start + timedelta(days=rental_days)

# CLient This Cloth Hand Over The Store And Finish This Contract
while True:
    try:
        return_date = datetime.strptime(
            input("Enter the actual return date (YYYY-MM-DD): "), "%Y-%m-%d"
        ).date()
        if return_date < rental_start:
            print("Return date cannot be before the rental start date.")
        else:
            break
    except ValueError:
        print("Please use the date format YYYY-MM-DD.")


cloth_name, daily_price = cloth_types[choice]
late_days = max(0, (return_date - due_date).days)
late_fee_per_day = daily_price * 0.10
rental_amount = daily_price * rental_days
late_fee = late_days * late_fee_per_day
total_amount = rental_amount + late_fee

print("\n========== RENTAL RECEIPT ==========")
print(f"Customer: {customer_name}")
print(f"Clothing: {cloth_name}")
print(f"Rental start date: {rental_start}")
print(f"Due date: {due_date}")
print(f"Actual return date: {return_date}")
print(f"Rental days: {rental_days}")
print(f"Price per day: Rs. {daily_price}")
print(f"Rental amount: Rs. {rental_amount:.2f}")
print(f"Late days: {late_days}")
print(f"Late fee: Rs. {late_fee:.2f}")
print(f"Total amount: Rs. {total_amount:.2f}")
print("Thank you for choosing Hermès!")
print("====================================")

 
# Electrical Bill Managment 
# Billing Company Name 
 
# Name: Muhammad Bilal
# Data Analysis Batch: 317
# Scenario: Electricity Bill Management System


FIXED_SURCHARGE = 150.00


def get_required_text(message):
    """Get text that is not empty."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("This field cannot be empty.")


def get_phone_number(message):
    """Get a phone number containing digits only."""
    while True:
        value = input(message).strip()
        if value.isdigit():
            return value
        print("Please enter a phone number using digits only.")


def get_non_negative_number(message):
    """Get a number that is zero or greater."""
    while True:
        try:
            value = float(input(message))
            if value >= 0:
                return value
            print("Please enter zero or a positive number.")
        except ValueError:
            print("Please enter a valid number.")


def get_current_reading(previous_reading):
    """Get a current reading that is not less than the previous reading."""
    while True:
        current_reading = get_non_negative_number(
            "Enter the current meter reading: "
        )
        if current_reading >= previous_reading:
            return current_reading
        print("Current reading cannot be less than the previous reading.")


def calculate_energy_charge(units_consumed):
    """Calculate the charge using three electricity usage tiers."""
    first_tier_units = min(units_consumed, 100)
    second_tier_units = min(max(units_consumed - 100, 0), 200)
    third_tier_units = max(units_consumed - 300, 0)

    first_tier_charge = first_tier_units * 10.00
    second_tier_charge = second_tier_units * 15.00
    third_tier_charge = third_tier_units * 20.00

    return first_tier_charge + second_tier_charge + third_tier_charge


print("========================================")
print("       ELECTRICITY BILL SYSTEM")
print("========================================")

customer_name = get_required_text("Enter customer name: ")
meter_number = get_required_text("Enter meter number: ")
address = get_required_text("Enter customer address: ")
phone_number = get_phone_number("Enter phone number: ")

previous_reading = get_non_negative_number(
    "Enter the previous meter reading: "
)
current_reading = get_current_reading(previous_reading)
units_consumed = current_reading - previous_reading

energy_charge = calculate_energy_charge(units_consumed)
total_bill = energy_charge + FIXED_SURCHARGE

print("\n============= BILL RECEIPT =============")
print(f"Customer name:       {customer_name}")
print(f"Meter number:        {meter_number}")
print(f"Address:             {address}")
print(f"Phone number:        {phone_number}")
print("-----------------------------------------")
print(f"Previous reading:    {previous_reading:.2f}")
print(f"Current reading:     {current_reading:.2f}")
print(f"Units consumed:      {units_consumed:.2f}")
print("-----------------------------------------")
print("Rate tiers:")
print("  First 100 units:   Rs. 10.00 per unit")
print("  Next 200 units:    Rs. 15.00 per unit")
print("  Above 300 units:   Rs. 20.00 per unit")
print(f"Energy charge:       Rs. {energy_charge:.2f}")
print(f"Fixed surcharge:     Rs. {FIXED_SURCHARGE:.2f}")
print(f"TOTAL BILL:          Rs. {total_bill:.2f}")
print("=========================================")
print("Thank you for using the electricity bill system.")

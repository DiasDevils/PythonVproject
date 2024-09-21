# connecting to gcp and having access to google sheets #
import gspread
from google.oauth2.service_account import Credentials

import re
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Vproject')

# code to check if getting data is working #

# delivery = SHEET.worksheet('delivery')
# data = delivery.get_all_values()
# print(data)


#  1. Function to Get delivery input from user. #
def get_delivery():
    print("Welcome to the Vaccine Stock Tracking System. This system is designed to help you efficiently monitor and manage your vaccine inventory. It provides real-time updates on vaccine deliveries, usage tracking, expiration dates, and usage reports, ensuring that you always have accurate records and can maintain optimal vaccine stock levels.")
    # Ask if the user wants to input delivery data
    response = input("Do you need to input DELIVERY data? (yes/no): ").strip().lower()
    
    # Exit this function if no deliveries
    if response == "no":
        print("Skipping delivery input...")
        return None  

    elif response == "yes":
        print("Please enter vaccine delivery data in steps.")
        
        # Batch number validation
        while True:
            try:
                batch = int(input("Step 1. Enter the batch number (integer): "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for the batch number.")
        
        # Date validation (dd/mm/yyyy format and not in the future)
        while True:
            date_str = input("Step 2. Enter the delivery date (dd/mm/yyyy): ")
            try:
                delivery_date = datetime.strptime(date_str, "%d/%m/%Y")
                if delivery_date > datetime.now():
                    print("The delivery date cannot be in the future. Please enter a valid date.")
                else:
                    break
            except ValueError:
                print("Invalid date format. Please enter the date in the format dd/mm/yyyy.")
        
        # Vaccine name validation
        valid_vaccines = ["flu-one", "flu-two"]
        while True:
            vaccine = input("Step 3. Enter the vaccine name (flu-one or flu-two): ").strip().lower()
            if vaccine in valid_vaccines:
                break
            else:
                print("Invalid vaccine name. Please enter 'flu-one' or 'flu-two'.")
        
        # Quantity validation
        while True:
            try:
                quantity = int(input("Step 4. Enter the quantity of vials (integer): "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for the quantity.")
        
        # Create dictionary to store the inputted data
        delivery_data = {
            "batch": batch, 
            "delivery_date": delivery_date.strftime("%d/%m/%Y"),
            "vaccine": vaccine,  
            "quantity": quantity
        }

        # Print confirmation
        print(f"The data you entered for delivery is Batch Number {batch}, delivered on {date_str}. The vaccine name is {vaccine} and the quantity is {quantity}")
        
        # Return the data dictionary
        return delivery_data
    # Re-run the function if the input is invalid
    else:
        print("Invalid input. Please answer with 'yes' or 'no'.")
        return get_delivery()  


def update_delivery(data):
    print("Updating deliveries...\n")
    delivery_worksheet = SHEET.worksheet('delivery')
    delivery_row = list(data.values())
    delivery_worksheet.append_row(delivery_row)
    print("Deliveries updated successfully!\n")
# Delivery data
data = get_delivery()

# Print the returned data (will print None if skipped)
if data:
    update_delivery(data)
    # print("Updated with delivery data:", data)
else:
    print("No delivery data updated.")







"""3. Get usage input from user"""
def get_usage():
    print("Now moving to the usage input...\n")
    response = input("Do you need to input USAGE data? (yes/no): ").strip().lower()

    if response == "no":
        print("Thank you for your custom. Come back soon. Goodbye!")
        return None
    elif response == "yes":
        print("Please enter vaccine usage data.")

        #Batch validation
        while True:
            try:
                batch= int(input("Enter the batch number (integer):"))
                break
            except ValueError:
                print("Invalid input: Please enter a valid integer for the batch number.")
        # Quantity Validation
        while True:
            try:
                quantity_used =int(input("Enter the quantity of vials used (integer):"))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for the quantity used. ")
        
        #Create usage dictionary to store data
        usage_data={
            "batch":batch,
            "quantity_used": quantity_used
        }
         # Print confirmation
        print(f"The data you entered for usage is Batch Number {batch} with {quantity_used} vials used.")
        return usage_data
    
    else:
        print("Invalid input. Please answer 'yes' or 'no'.")
        return get_usage()


def update_use(data):
    print("Updating used vaccines data...\n")
    use_worksheet = SHEET.worksheet('used')
    use_row = list(data.values())
    use_worksheet.append_row(use_row)
    print("Used vaccines data updated successfully!\n")
# Delivery data
data = get_usage()

# Print the returned data (will print None if skipped)
if data:
    update_use(data)
    # print("Updated with used vaccines data:", data)
else:
    print("No used vaccine data updated.")        


""" connecting to gcp and having access to google sheets"""
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

""" code to check if getting data is working """
# delivery = SHEET.worksheet('delivery')
# data = delivery.get_all_values()
# print(data)


"""1. Get delivery input from user"""
def get_delivery():
    # Ask if the user wants to input delivery data
    print("Welcome to the Vaccine Stock Tracking System. This system is designed to help you efficiently monitor and manage your vaccine inventory. It provides real-time updates on vaccine deliveries, usage tracking, expiration dates, and usage reports, ensuring that you always have accurate records and can maintain optimal vaccine stock levels.")
    response = input("Do you need to input delivery data? (yes/no): ").strip().lower()
    
    if response == "no":
        print("Skipping delivery input...")
        return  # Exit this function if the user chooses to skip delivery

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
        
        # Print confirmation
        print(f"The data you entered for delivery is Batch {batch}, delivered on the {date_str}. The vaccine name is {vaccine} and the quantity is {quantity}")
    else:
        print("Invalid input. Please answer with 'yes' or 'no'.")
        get_delivery()  # Re-run the function if the input is invalid

"""2. Get usage input from user"""
def get_usage():
    # Placeholder function to show what comes next
    print("Now moving to the usage input...")

# Call the function to start the process
get_delivery()
get_usage()

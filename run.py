import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from tabulate import tabulate
import gspread
import re

# Load credentials from environment variable
credentials_info = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

# Initialize your Google Sheets API client using credentials_info
credentials = Credentials.from_service_account_info(credentials_info)
SHEET = build('sheets', 'v4', credentials=credentials).spreadsheets()

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_info(json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS']))
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Vproject')

''' """"""""""""""""""""""""""""""""""""""""" '''
#  1. Function to Get delivery input from user. #
''' """"""""""""""""""""""""""""""""""""""""" '''


def get_delivery():
    response = input("Please confirm: Do you need to input DELIVERY data?('yes/no'): ").strip().lower()
    if response == "no":
        print("Skipping delivery input...")
        return None
    elif response == "yes":
        print("Please enter vaccine delivery data in steps.")

        # Batch validation
        while True:
            try:
                batch = int(input("Step 1. Enter batch number (Number 1-100): "))
                if 1 <= batch <= 100:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 100.")
            except ValueError:
                print("Invalid input. Please enter a valid batch number.")

        # Date validation (dd/mm/yyyy format and not in the future)
        while True:
            date_str = input("Step 2. Enter delivery date in format (dd/mm/yyyy): ")
            try:
                delivery_date = datetime.strptime(date_str, "%d/%m/%Y")
                if delivery_date > datetime.now():
                    print("Delivery date cannot be in future. Please enter a valid date.")
                elif delivery_date < datetime(2023, 1, 1):
                    print("Delivery date cannot be earlier than 01/01/2023. Please enter a valid date.")
                else:
                    break
            except ValueError:
                print("Invalid date format. Please enter the date in format dd/mm/yyyy.")

        # Vaccine name validation
        valid_vaccines = ["flu-one", "flu-two"]
        while True:
            vaccine = input("Step 3. Enter vaccine name (flu-one or flu-two): ").strip().lower()
            if vaccine in valid_vaccines:
                break
            else:
                print("Invalid vaccine name. Please enter 'flu-one' or 'flu-two'.")

        # Quantity validation
        while True:
            try:
                quantity = int(input("Step 4. Enter quantity of vials delivered (Number 1-50): "))
                if 1 <= quantity <= 50:
                    break
                else:
                    print("Invalid input. Please enter quantity between 1 and 50.")
            except ValueError:
                print("Invalid input. Please enter valid quantity number.")

        # Create dictionary to store the inputted data
        delivery_data = {
            "batch": batch,
            "delivery_date": delivery_date.strftime("%d/%m/%Y"),
            "vaccine": vaccine,
            "quantity": quantity
        }

        # Print confirmation
        print(f"Delivery Data Entered: \n Batch Number: {batch}\n Delivered date: {date_str}\n Vaccine name: {vaccine} \n Quantity: {quantity}")

        # Return the data dictionary
        return delivery_data
    else:
        print("Invalid input. Please answer 'yes' or 'no'.")
        return get_delivery()

# Function to update the delivery worksheet


def update_delivery(data):
    print("Updating deliveries...\n")
    delivery_worksheet = SHEET.worksheet('delivery')
    delivery_row = list(data.values())
    delivery_worksheet.append_row(delivery_row)
    print("Deliveries updated successfully!\n")


''' """"""""""""""""""""""""""""""""""""""""" '''
# 2. Get usage input from user #
''' """"""""""""""""""""""""""""""""""""""""" '''
def get_usage():
    # Retrieve the current delivery and usage data from the worksheets
    delivery_worksheet = SHEET.worksheet('delivery')
    delivery_data = delivery_worksheet.get_all_values()[1:]  # Skip headers

    usage_worksheet = SHEET.worksheet('used')
    usage_data = usage_worksheet.get_all_values()[1:]  # Skip headers

    # Calculate total delivered quantities for each batch and vaccine
    delivery_sums = {}
    for row in delivery_data:
        batch = row[0]
        vaccine = row[2]
        quantity = int(row[3])

        key = (batch, vaccine)
        if key in delivery_sums:
            delivery_sums[key] += quantity
        else:
            delivery_sums[key] = quantity

    # Calculate total used quantities for each batch and vaccine
    usage_sums = {}
    for row in usage_data:
        batch = row[0]
        vaccine = row[1]
        quantity_used = int(row[2])

        key = (batch, vaccine)
        if key in usage_sums:
            usage_sums[key] += quantity_used
        else:
            usage_sums[key] = quantity_used

    # Get user input for usage
    while True:
        batch = input("Enter batch number for usage: ").strip()
        vaccine = input("Enter the vaccine name for usage ('flu-one' or 'flu-two'): ").strip().lower()
        
        if (batch, vaccine) not in delivery_sums:
            print("Error: No matching delivery record found for this batch and vaccine. Please try again.")
            continue

        # Get quantity used from user
        while True:
            try:
                quantity_used = int(input(f"Enter the quantity used for batch {batch} (vaccine: {vaccine}): "))
                if quantity_used <= 0:
                    print("Error: Quantity used must be a positive number. Please try again.")
                    continue
                break
            except ValueError:
                print("Error: Invalid input. Please enter a valid number.")
        
        # Check if the total usage exceeds the total delivered quantity
        total_used = usage_sums.get((batch, vaccine), 0) + quantity_used
        total_delivered = delivery_sums[(batch, vaccine)]

        if total_used > total_delivered:
            print(f"Error: The total usage ({total_used}) exceeds the total delivered quantity ({total_delivered}) for batch {batch} and vaccine {vaccine}. Please try again.")
        else:
            # Update the usage data
            usage_data = {
                "batch": batch,
                "vaccine": vaccine,
                "quantity_used": quantity_used
            }
            print(f"Usage for batch {batch} (vaccine: {vaccine}) successfully recorded.")
            return usage_data


''' """"""""""""""""""""""""""""""""""""""""" '''
# Function to update the usage worksheet
''' """"""""""""""""""""""""""""""""""""""""" '''


def update_use(data):
    print("Updating used vaccines data...\n")
    use_worksheet = SHEET.worksheet('used')
    use_row = list(data.values())
    use_worksheet.append_row(use_row)
    print("Used vaccines data updated successfully!\n")


''' """"""""""""""""""""""""""""""""""""""""" '''
# 3. Calculating stock from delivery and usage #
''' """"""""""""""""""""""""""""""""""""""""" '''


def calculate_stock():
    delivery_worksheet = SHEET.worksheet('delivery')
    delivery_data = delivery_worksheet.get_all_values()[1:]

    usage_worksheet = SHEET.worksheet('used')
    usage_data = usage_worksheet.get_all_values()[1:]

    delivery_sums = {}
    latest_delivery_dates = {}
    usage_sums = {}

    for row in delivery_data:
        batch = row[0]
        delivery_date = datetime.strptime(row[1], "%d/%m/%Y")
        vaccine = row[2]
        quantity = int(row[3])

        key = (batch, vaccine)

        if key in delivery_sums:
            delivery_sums[key] += quantity
        else:
            delivery_sums[key] = quantity

        if key in latest_delivery_dates:
            if delivery_date > latest_delivery_dates[key]:
                latest_delivery_dates[key] = delivery_date
        else:
            latest_delivery_dates[key] = delivery_date

    for row in usage_data:
        batch = row[0]
        vaccine = row[1]
        quantity_used = int(row[2])

        key = (batch, vaccine)

        if key in usage_sums:
            usage_sums[key] += quantity_used
        else:
            usage_sums[key] = quantity_used

    stock_data = []
    for key, delivered_qty in delivery_sums.items():
        batch, vaccine = key
        used_qty = usage_sums.get(key, 0)
        stock_left = delivered_qty - used_qty

        last_delivery_date = latest_delivery_dates[key]
        expiry_date = last_delivery_date + timedelta(days=30)

        last_delivery_str = last_delivery_date.strftime("%d/%m/%Y")
        expiry_date_str = expiry_date.strftime("%d/%m/%Y")

        today = datetime.today()
        status = "Expired" if expiry_date <= today else "In Date"

        stock_data.append([batch, vaccine, delivered_qty, used_qty, stock_left, last_delivery_str, expiry_date_str, status])

    return stock_data


''' """""""""""""""""""""""""""" '''
# Updating stock function #
''' """""""""""""""""""""""""""" '''


def update_stock(stock_data):
    print("Retrieving stock data...\n")
    stock_worksheet = SHEET.worksheet('stock')
    stock_worksheet.clear()
    headers = ['B', 'VN', 'DQ', 'UQ', 'SK', 'LDD', 'ED', "ST"]
    stock_worksheet.append_row(headers)

    for row in stock_data:
        stock_worksheet.append_row(row)
    print("Stock data retrieved successfully!\n")
    print("Please see Vaccine Stock table below.\n")

    print("Important to know:\n")
    print("B   = Batch Number         ||  VN = Vaccine Name")
    print("DQ  = Delivered Quantity   ||  UQ = Used Quantity")
    print("SK  = Stock Available Now  ||  ST = Status ")
    print("LDD = Last Delivery Date   ||  ED = Expiry Date \n")
    print("Current Stock Data:")
    print(tabulate(stock_data, headers=headers, tablefmt='grid'))


''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# 4. Main function to handle workflow #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''


def main_menu():
    print("Welcome to the Flu Vaccine Stock Tracking System (FVST)")

    while True:
        print("Please follow instructions for the FVST System below.")
        print('---------------------')
        print('Menu:')
        print('---------------------')
        print('Option 1.Input Delivery Data')
        print('Option 2.Input Usage Data')
        print('Option 3.View Stock Table')
        print('Option 4.Exit')
        print('---------------------')
        choice = input('Please Select Option 1,2,3 or 4 to continue:')
        if choice == '1':
            delivery_data = get_delivery()
            if delivery_data:
                update_delivery(delivery_data)
        elif choice == '2':
            usage_data = get_usage()
            if usage_data:
                update_use(usage_data)
        elif choice == '3':
            stock_data = calculate_stock()
            if stock_data:
                update_stock(stock_data)
            else:
                print("No new stock data to update. \n")
        elif choice == '4':
            print('Thank you and goodbye!')
            break
        else:
            print('Please choose a valid option between 1-4.')


''' """"""""""""""""""""""""""""""""""""""""" '''
# 4. Call workflow #
''' """"""""""""""""""""""""""""""""""""""""" '''


def main():
    main_menu()


main()

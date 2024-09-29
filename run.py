''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# connecting to gcp and having access to google sheets #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''

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
# CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Vproject')


# code to check if getting data is working #
# delivery = SHEET.worksheet('delivery')
# data = delivery.get_all_values()
# print(data)


''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
#  1. Function to Get delivery input from user. #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
def get_delivery():
    print("Welcome to the Flu Vaccine Stock Tracking System.")
    response = input("Do you need to input DELIVERY data? (yes/no): ").strip().lower()
    
    if response == "no":
        print("Skipping delivery input...")
        return None  
    elif response == "yes":
        print("Please enter vaccine delivery data in steps.")
        
        # Batch validation
        while True:
            try:
                batch = int(input("Step 1. Enter the batch number (Number between 1 and 100): "))
                if 1 <= batch <= 100:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 100.")
            except ValueError:
                print("Invalid input. Please enter a valid number for the batch.")
        
        # Date validation (dd/mm/yyyy format and not in the future)
        while True:
            date_str = input("Step 2. Enter the delivery date (dd/mm/yyyy) from 2020 onwards: ")
            try:
                delivery_date = datetime.strptime(date_str, "%d/%m/%Y")
                if delivery_date > datetime.now():
                    print("The delivery date cannot be in the future. Please enter a valid date.")
                elif delivery_date < datetime (2020,1,1):
                    print:("The delivery date cannot be earlier than 2020. Please enter a valid date.")
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
                quantity = int(input("Step 4. Enter the quantity of vials (Whole number): "))
                if 1 <= quantity <= 50:
                    break
                else:
                    print("Invalid input. Please enter a quantity between 1 and 50.")
            except ValueError:
                print("Invalid input. Please enter a valid number for the quantity.")
        
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
    else:
        print("Invalid input. Please answer with 'yes' or 'no'.")
        return get_delivery()  

# Function to update the delivery worksheet
def update_delivery(data):
    print("Updating deliveries...\n")
    delivery_worksheet = SHEET.worksheet('delivery')
    delivery_row = list(data.values())
    delivery_worksheet.append_row(delivery_row)
    print("Deliveries updated successfully!\n")


''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# 2. Get usage input from user #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
def get_usage():
    print("Now moving to the used vaccines input...\n")
    response = input("Do you need to input USAGE data? (yes/no): ").strip().lower()

    if response == "no":
        print("Skipping usage input.")
        return None
    elif response == "yes":
        print("Please enter vaccine usage data.")

        # Batch validation
        while True:
            try:
                batch= int(input("Enter the batch number (Number between 1 and 100):"))
                if 1 <= batch <= 100:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 100.")
            except ValueError:
                print("Invalid input: Please enter a valid number for the batch.")

        # Vaccine name validation
        valid_vaccines = ["flu-one", "flu-two"]
        while True:
            vaccine = input("Step 3. Enter the vaccine name (flu-one or flu-two): ").strip().lower()
            if vaccine in valid_vaccines:
                break
            else:
                print("Invalid vaccine name. Please enter 'flu-one' or 'flu-two'.")

        # Quantity Validation
        while True:
            try:
                quantity_used = int(input("Enter the quantity of vials used (Whole Number):"))
                if 1 <= quantity_used <= 50:
                    break
                else:
                    print("Invalid input. Please enter quantity between 1 and 50.")
            except ValueError:
                print("Invalid input. Please enter a valid number for the quantity used.")
        
        # Create usage dictionary to store data
        usage_data = {
            "batch": batch,
            "vaccine": vaccine,  
            "quantity_used": quantity_used
        }

        # Print confirmation
        print(f"The data you entered for usage is Batch Number {batch} of vaccine name {vaccine} with {quantity_used} vials used.")
        return usage_data
    else:
        print("Invalid input. Please answer 'yes' or 'no'.")
        return get_usage()

# Function to update the usage worksheet
def update_use(data):
    print("Updating used vaccines data...\n")
    use_worksheet = SHEET.worksheet('used')
    use_row = list(data.values())
    use_worksheet.append_row(use_row)
    print("Used vaccines data updated successfully!\n")


''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# 3. Calculating stock from delivery and usage #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
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

def update_stock(stock_data):
    print("Updating stock data...\n")
    stock_worksheet = SHEET.worksheet('stock')
    stock_worksheet.clear()
    headers = ['B', 'VN', 'DQ', 'UQ', 'SK', 'LDD', 'ED', "ST"]
    stock_worksheet.append_row(headers)
    
    for row in stock_data:
        stock_worksheet.append_row(row)
    print("Stock data updated successfully!\n")
    print("Please see Vaccine Stock table below.\n")

    
    print("Important to know:\n")
    print ("B   = Batch Number         ||  VN = Vaccine Name" )
    print ("DQ  = Delivered Quantity   ||  UQ = Used Quantity")
    print ("SK  = Stock Available Now  ||  ST = Status ")
    print ("LDD = Last Delivery Date   ||  ED = Expiry Date \n")
    print("Current Stock Data:")
    print(tabulate(stock_data, headers=headers, tablefmt='grid'))

''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# 4. Main function to handle workflow #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
def main():
    # Get delivery data
    delivery_data = get_delivery()
    if delivery_data:
        update_delivery(delivery_data)
    
    # Get usage data
    usage_data = get_usage()
    if usage_data:
        update_use(usage_data)

    # Calculate and update stock data
    stock_data = calculate_stock()
    if stock_data:
        update_stock(stock_data)
    else:
        print("No new stock data to update.\n")

# Run the main function
main()

#
# if used qty > del qty throw an error
# if used vac does not have deliv data print that it wont show in table
# unless delivery equivalent is entered
#

# ############### DEPLOYED ##########################

''' """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" '''
# Connecting to gcp and having access to google sheets and importing required libraries
''' """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" '''
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from tabulate import tabulate

# Load credentials from environment variable
credentials_info = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

# Initialize your Google Sheets API client using credentials_info
credentials = Credentials.from_service_account_info(credentials_info)
SHEET = build('sheets', 'v4', credentials=credentials).spreadsheets()

import gspread
import re

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


''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
#  1. Function to Get delivery input from user. #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
def get_delivery():
    # print("Welcome to the Flu Vaccine Stock Tracking System.")
    response = input("Please confirm: Do you need to input DELIVERY data? ('yes/no'): ").strip().lower()
    
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
            date_str = input("Step 2. Enter the delivery date in format (dd/mm/yyyy): ")
            try:
                delivery_date = datetime.strptime(date_str, "%d/%m/%Y")
                if delivery_date > datetime.now():
                    print("The delivery date cannot be in the future. Please enter a valid date.")
                elif delivery_date < datetime (2023,1,1):
                    print("The delivery date cannot be earlier than 01/01/2023. Please enter a valid date.")
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
                quantity = int(input("Step 4. Enter the quantity of vials delivered (Whole number): "))
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
    # print("Now moving to the used vaccines input...\n")
    response = input("Please confirm: Do you need to input USAGE data? ('yes/no'): ").strip().lower()

    if response == "no":
        print("Skipping usage input.")
        return None
    elif response == "yes":
        print("Please enter vaccine usage data.")

       # Batch validation
        while True:
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
            # Retrieve delivered quantity for the specified batch and vaccine
            delivery_worksheet = SHEET.worksheet('delivery')
            delivery_data = delivery_worksheet.get_all_values()[1:] 
            delivered_quantity = 0
            # Check if the batch and vaccine combination exists in delivery
            for row in delivery_data:
                if int(row[0]) == batch and row[2] == vaccine:
                    delivered_quantity += int(row[3]) 
            # Check if there's no delivery data for the batch and vaccine
            if delivered_quantity == 0:
                print(f"No delivery data found for Batch {batch} and Vaccine {vaccine}. Please enter a valid usage.")
                #return None  # Exit if there's no delivery data
                continue

            # Quantity Validation Loop
            while True:
                try:
                    quantity_used = int(input("Enter the quantity of vials used (Whole Number):"))
                    if quantity_used < 1:
                        print("Quantity used must be at least 1.")
                    elif quantity_used > 50:
                        print("Quantity used must not exceed 50.")
                    elif quantity_used > delivered_quantity:
                         print(f"Quantity used cannot exceed the delivered quantity of {delivered_quantity}.")
                    else:
                        break
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
# def main():
#     # Get delivery data
#     delivery_data = get_delivery()
#     if delivery_data:
#         update_delivery(delivery_data)
    
#     # Get usage data
#     usage_data = get_usage()
#     if usage_data:
#         update_use(usage_data)

#     # Calculate and update stock data
#     stock_data = calculate_stock()
#     if stock_data:
#         update_stock(stock_data)
#     else:
#         print("No new stock data to update.\n")

# # Run the main function
# main()

def main_menu():
    print("Welcome to the Flu Vaccine Stock Tracking System (FVST)")

    while True:
        print("Please follow instructions for the FVST System below.")
        print('---------------------')
        print('Option 1.INPUT DELIVERIES (accepts dates from 01/01/2023 & quantities 1 to 50)')
        print('---------------------')
        print('Option 2.INPUT USAGE (usage cannot exceed delivery per batch)')
        print('---------------------')
        print('Option 3. VIEW STOCK TABLE (shows stock details)')
        print('---------------------')
        print('Option 4. EXIT (logs out of FVST)')
        print('---------------------')
        choice= input('Please Select Option 1,2,3 or 4 to continue:')
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
            print ('Thank you and goodbye!')    
            break
        else:
            print('Please choose a valid option between 1-4.')
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# 4. Call workflow #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
def main():
    main_menu()
main()

# ######################################## END ################################# # 

# ######################################## 29/09/2024 START WORKS with MAIN MENU ################################# # 


''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# Connecting to gcp and having access to google sheets #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from tabulate import tabulate

# Load credentials from environment variable
credentials_info = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

# Initialize your Google Sheets API client using credentials_info
credentials = Credentials.from_service_account_info(credentials_info)
SHEET = build('sheets', 'v4', credentials=credentials).spreadsheets()

import gspread
import re

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
    response = input("Do you need to input DELIVERY data? (Please answer 'yes/no'): ").strip().lower()
    
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
            date_str = input("Step 2. Enter the delivery date (dd/mm/yyyy) from the year 2020 onwards: ")
            try:
                delivery_date = datetime.strptime(date_str, "%d/%m/%Y")
                if delivery_date > datetime.now():
                    print("The delivery date cannot be in the future. Please enter a valid date.")
                elif delivery_date < datetime (2020,1,1):
                    print("The delivery date cannot be earlier than 2020. Please enter a valid date.")
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
    response = input("Do you need to input USAGE data? (Please answer 'yes/no'): ").strip().lower()

    if response == "no":
        print("Skipping usage input.")
        return None
    elif response == "yes":
        print("Please enter vaccine usage data.")

       # Batch validation
        while True:
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
            # Retrieve delivered quantity for the specified batch and vaccine
            delivery_worksheet = SHEET.worksheet('delivery')
            delivery_data = delivery_worksheet.get_all_values()[1:] 
            delivered_quantity = 0
            # Check if the batch and vaccine combination exists in delivery
            for row in delivery_data:
                if int(row[0]) == batch and row[2] == vaccine:
                    delivered_quantity += int(row[3]) 
            # Check if there's no delivery data for the batch and vaccine
            if delivered_quantity == 0:
                print(f"No delivery data found for Batch {batch} and Vaccine {vaccine}. Please enter a valid usage.")
                #return None  # Exit if there's no delivery data
                continue

            # Quantity Validation Loop
            while True:
                try:
                    quantity_used = int(input("Enter the quantity of vials used (Whole Number):"))
                    if quantity_used < 1:
                        print("Quantity used must be at least 1.")
                    elif quantity_used > 50:
                        print("Quantity used must not exceed 50.")
                    elif quantity_used > delivered_quantity:
                         print(f"Quantity used cannot exceed the delivered quantity of {delivered_quantity}.")
                    else:
                        break
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
# def main():
#     # Get delivery data
#     delivery_data = get_delivery()
#     if delivery_data:
#         update_delivery(delivery_data)
    
#     # Get usage data
#     usage_data = get_usage()
#     if usage_data:
#         update_use(usage_data)

#     # Calculate and update stock data
#     stock_data = calculate_stock()
#     if stock_data:
#         update_stock(stock_data)
#     else:
#         print("No new stock data to update.\n")

# # Run the main function
# main()

def main_menu():
    print("Welcome to the Flu Vaccine Stock Tracking System")

    while True:
        print('---------------------')
        print('Option 1. Input Delivery Data.')
        print('Option 2. Input Usage Data.')
        print('Option 3. View Vaccine Stock')
        print('Option 4. Exit')

        choice= input('Please select an option (1-4):')
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
            print ('Thank you and goodbye!')    
            break
        else:
            print('Please choose a valid option between 1-4.')
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# 4. Call workflow #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
def main():
    main_menu()
main()


# ######################################## END ################################# # 



# ###################### 28/09/2024 START ############################ # 

''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# connecting to gcp and having access to google sheets #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''

import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from tabulate import tabulate

# Load credentials from environment variable
credentials_info = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

# Initialize your Google Sheets API client using credentials_info
credentials = Credentials.from_service_account_info(credentials_info)
SHEET = build('sheets', 'v4', credentials=credentials).spreadsheets()

''' from up above is new''' 
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# connecting to gcp and having access to google sheets #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''

import gspread
from google.oauth2.service_account import Credentials
import re
from datetime import datetime, timedelta
from tabulate import tabulate


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
                batch= int(input("Enter the batch number (integer):"))
                break
            except ValueError:
                print("Invalid input: Please enter a valid integer for the batch number.")

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
                quantity_used = int(input("Enter the quantity of vials used (integer):"))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for the quantity used.")
        
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



# ################################# END ############################## # 

""" """" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" """" """
""" get delivery input from user """
def get_delivery():
    print("Please enter vaccine delivery data.")
    print("Please enter the batch number. For example: 1")
    d_str1= input("Enter your batch here:")

    print("Please enter the delivery month in date format. For example 31/12/2024")
    d_str2= input("Enter date here:")

    print("Please enter the vaccine name. Accepts valid vaccines only: flu-one or flu-two")
    d_str3= input("Enter vaccine name here:")

    print("Please enter the quantity of vials delivered: For example: 20")
    d_str4= input("Enter quantity here:")

    print(f"The data you entered for delivery is Batch {d_str1}, on the {d_str2}, vaccine name {d_str3}, quantity {d_str4}")

get_delivery()


""" """" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" """" """

""" get delivery input from user """
def get_delivery():
    print("Please enter vaccine delivery data in the following format:")
    print("Batch number, Date (dd/mm/yyyy), Vaccine name, Quantity")
    print("For example: 1, 31/12/2024, flu-one, 20")

    # Get all inputs at once as a comma-separated string
    delivery_input = input("Enter your delivery data here: ")

    # Split the input string into a list by commas
    delivery_data = delivery_input.split(',')

    # Strip any extra spaces around each input
    batch = delivery_data[0].strip()
    date = delivery_data[1].strip()
    vaccine = delivery_data[2].strip()
    quantity = delivery_data[3].strip()

    print(f"The data you entered for delivery is Batch {batch}, on the {date}, vaccine name {vaccine}, quantity {quantity}")

get_delivery()


""" """" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" """" """
""" this allows dates in future """
def get_delivery():
    # Batch number validation
    while True:
        try:
            batch = int(input("Enter the batch number (integer): "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for the batch number.")
    
    # Date validation (dd/mm/yyyy format)
    while True:
        date_str = input("Enter the delivery date (dd/mm/yyyy): ")
        try:
            # Try to parse the date
            datetime.strptime(date_str, "%d/%m/%Y")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in the format dd/mm/yyyy.")
    
    # Vaccine name validation
    valid_vaccines = ["flu-one", "flu-two"]
    while True:
        vaccine = input("Enter the vaccine name (flu-one or flu-two): ").strip().lower()
        if vaccine in valid_vaccines:
            break
        else:
            print("Invalid vaccine name. Please enter 'flu-one' or 'flu-two'.")
    
    # Quantity validation
    while True:
        try:
            quantity = int(input("Enter the quantity of vials (integer): "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer for the quantity.")
    
    # Final confirmation of data
    print(f"The data you entered for delivery is Batch {batch}, on the {date_str}, vaccine name {vaccine}, quantity {quantity}")

# Call the function to get user input
get_delivery()





""" this code works perfect """ 
""" """" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" """" """

def get_delivery():
    print("Please enter vaccine delivery data in steps.")
    # Batch number validation
    while True:
        try:
            batch = int(input("Step1. Enter the batch number (integer): "))
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
    print(f"The data you entered for delivery is Batch {batch}, on the {date_str}, vaccine name {vaccine}, quantity {quantity}")


get_delivery()







""" this code works perfect but i dont get the data returned in a dictionary and i need a dictionary """ 
""" """" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" """" """
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


""" """" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" """" """
# calculate stock but no delivery date accounted for
def calculate_stock():
    # Get all delivery data from the 'delivery' sheet
    delivery_worksheet = SHEET.worksheet('delivery')
    # Skip header row
    delivery_data = delivery_worksheet.get_all_values()[1:]  
    
    # Get all usage data from the 'used' sheet
    usage_worksheet = SHEET.worksheet('used')
    usage_data = usage_worksheet.get_all_values()[1:]

    # Create dictionaries to hold summed values for delivery and used
    delivery_sums = {}
    usage_sums = {}

    # Sum delivery data by batch and vaccine name with unique key
    for row in delivery_data:
        batch = row[0]
        vaccine = row[2]
        quantity = int(row[3])
        # Key based on batch and vaccine
        key = (batch, vaccine)  
        if key in delivery_sums:
            delivery_sums[key] += quantity
        else:
            delivery_sums[key] = quantity

    # Sum usage data by batch and vaccine name
    for row in usage_data:
        batch = row[0] 
        vaccine = row[1]
        quantity_used = int(row[2])
        # Key based on batch and vaccine
        key = (batch, vaccine)  
        if key in usage_sums:
            usage_sums[key] += quantity_used
        else:
            usage_sums[key] = quantity_used

    # Calculate the stock left (delivery - used)
    stock_data = []
    for key, delivered_qty in delivery_sums.items():
        batch, vaccine = key
        # If no usage, treat it as 0
        used_qty = usage_sums.get(key, 0)  
        stock_left = delivered_qty - used_qty
        stock_data.append([batch, vaccine, delivered_qty, used_qty, stock_left])

    return stock_data
stock = calculate_stock()
print(f"Your stock is {stock}")


""" '''''''''''''''''''''''''''''''''''''''''''''''''''''''''' """
''' glitch '''
# ''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# # connecting to gcp and having access to google sheets #
# ''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# import gspread
# from google.oauth2.service_account import Credentials

# import re
# from datetime import datetime
# from datetime import timedelta

# SCOPE = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive.file",
#     "https://www.googleapis.com/auth/drive"
#     ]

# CREDS = Credentials.from_service_account_file('creds.json')
# SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# SHEET = GSPREAD_CLIENT.open('Vproject')


# code to check if getting data is working #
# delivery = SHEET.worksheet('delivery')
# data = delivery.get_all_values()
# print(data)


''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
#  1. Function to Get delivery input from user. #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
def get_delivery():
    print("Welcome to the Vaccine Stock Tracking System. This system is designed to help you efficiently monitor and manage your vaccine inventory. It provides real-time updates on vaccine deliveries, usage tracking, expiration dates, and usage reports, ensuring that you always have accurate records and can maintain optimal vaccine stock levels.\n")
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






''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# 2. Get usage input from user #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
def get_usage():
    print("Now moving to the usage input...\n")
    response = input("Do you need to input USAGE data? (yes/no): ").strip().lower()

    if response == "no":
        print("Thank you for your using the system. Goodbye!")
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
                quantity_used =int(input("Enter the quantity of vials used (integer):"))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer for the quantity used. ")
        
        #Create usage dictionary to store data
        usage_data={
            "batch":batch,
            "vaccine": vaccine,  
            "quantity_used": quantity_used
        }
         # Print confirmation
        print(f"The data you entered for usage is Batch Number {batch} of vaccine name {vaccine} with {quantity_used} vials used.")
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


''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# 3. Calculating stock from delivery and usage #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''

def calculate_stock():
    # Get all delivery data from the 'delivery' sheet
    delivery_worksheet = SHEET.worksheet('delivery')
    # Skip header row
    delivery_data = delivery_worksheet.get_all_values()[1:]  
    
    # Get all usage data from the 'used' sheet
    usage_worksheet = SHEET.worksheet('used')
    usage_data = usage_worksheet.get_all_values()[1:] 

    # Create dictionaries to hold summed values for delivery and used
    delivery_sums = {}
    latest_delivery_dates = {}
    usage_sums = {}

    # Sum delivery data by batch and vaccine name
    for row in delivery_data:
        batch = row[0]
        delivery_date = datetime.strptime(row[1], "%d/%m/%Y")
        vaccine = row[2]
        quantity = int(row[3])
    
        key = (batch, vaccine)  

        # Update delivery sums
        if key in delivery_sums:
            delivery_sums[key] += quantity
        else:
            delivery_sums[key] = quantity

        # Track the latest delivery date
        if key in latest_delivery_dates:
            if delivery_date > latest_delivery_dates[key]:
                latest_delivery_dates[key] = delivery_date
        else:
            latest_delivery_dates[key] = delivery_date

    # Sum usage data by batch and vaccine as well
    for row in usage_data:
        batch = row[0] 
        vaccine = row[1]
        quantity_used = int(row[2])

        key = (batch, vaccine)

        # Update usage sums
        if key in usage_sums:
            usage_sums[key] += quantity_used
        else:
            usage_sums[key] = quantity_used

    # Calculate stock left (delivery - used)
    stock_data = []
    for key, delivered_qty in delivery_sums.items():
        batch, vaccine = key
        # If no usage, treat it as 0
        used_qty = usage_sums.get(key, 0)  
        stock_left = delivered_qty - used_qty

        # Get the latest delivery date and calculate expiry date (30 days shelf life)
        last_delivery_date = latest_delivery_dates[key]
        expiry_date = last_delivery_date + timedelta(days=30)

        # Format the dates to dd/mm/yyyy
        last_delivery_str = last_delivery_date.strftime("%d/%m/%Y")
        expiry_date_str = expiry_date.strftime("%d/%m/%Y")

        stock_data.append([batch, vaccine, delivered_qty, used_qty, stock_left, last_delivery_str, expiry_date_str])

    return stock_data


def update_stock(stock_data):
    print("Updating stock data...\n")
    stock_worksheet = SHEET.worksheet('stock')
    stock_worksheet.clear()
    headers = ['Batch Number', 'Vaccine Name', 'Delivered Quantity', 'Used Quantity', 'Stock Left', 'Last Delivery Date', 'Expiry Date']
    stock_worksheet.append_row(headers)
    
    # Loop through the stock data and append each row
    for row in stock_data:
        stock_worksheet.append_row(row)
    print("Stock data updated successfully!\n")

stock_data = calculate_stock()

# DOES NOT WORK
# Update the stock sheet with the calculated stock data
# if stock_data:
#     update_stock(stock_data)
# else:
#     print("No new stock updated.")


# stock = calculate_stock()
# print(f"Your stock is {stock}")

''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
# 4. Main function to handle workflow #
''' """"""""""""""""""""""""""""""""""""""""""""""""" '''
def main():
    # Delivery
    delivery_data = get_delivery()
    # Used
    usage_data = get_usage()

    # If both delivery and used are No, skip stock update
    if not delivery_data and not usage_data:
        print("No delivery or usage data entered. Stock update skipped.\n")
        return

    # Only proceed if there’s actual stock data to update
    if stock_data:
        update_stock(stock_data)
    else:
        print("No new stock data to update.\n")

main()


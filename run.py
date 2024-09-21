""" connecting to gcp and having access to google sheets"""
import gspread
from google.oauth2.service_account import Credentials

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


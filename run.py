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
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



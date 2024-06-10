import random
import datetime

# def generate_HR_credentials(firstname, lastname):
#     username = f"{firstname[:2]}{lastname[:2]}{random.randint(20, 70)}"
#     return username

# def generate_HR_credentials(firstname, lastname):
#     current_year = datetime.date.today().year
#     last_two_digits = str(current_year)[-2:]
#     username = f"{firstname[:2]}{lastname[:2]}{last_two_digits}"
#     return username
import datetime

# def generate_HR_credentials(firstname, lastname):
#     current_year = datetime.date.today().year
#     last_two_digits = str(current_year)[-2:]
#     current_month = str(datetime.date.today().month).zfill(2)
#     username = f"{firstname[:2]}{lastname[:2]}{last_two_digits}{current_month}"
#     return username
serial_number = 1  # initialize a serial number

def generate_HR_credentials(firstname, lastname):
    global serial_number  # access the global serial number
    current_year = datetime.date.today().year
    last_two_digits = str(current_year)[-2:]
    current_month = str(datetime.date.today().month).zfill(2)
    username = f"{firstname[:2]}{lastname[:2]}{last_two_digits}{current_month}{serial_number:03d}"
    serial_number += 1  # increment the serial number for the next username
    return username

fname = input("Enter Your Fname-> ")
lname = input("Enter Your Lname-> ")
firstname = fname.upper()
lastname = lname.upper()

y = generate_HR_credentials(firstname, lastname)

print(y)
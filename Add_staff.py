from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import motor.motor_asyncio as aiomotor
from passlib.hash import bcrypt
import random
import string
import smtplib
from email.message import EmailMessage

app = FastAPI()

# Connect to MongoDB
client = aiomotor.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["mydatabase"]
users_collection = db["users"]



# Hash the password
def hash_password(password):
    return bcrypt.hash(password)

# # Send email with the credentials
def send_email(email, username, password):
    msg = EmailMessage()
    msg.set_content(f'{username},{password}')

    msg['Subject'] = 'Staff Account Credentials'
    msg['From'] = 'mygmail@example.com'
    msg['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.login('mygmail@example.com', 'gmail password')
        server.send_message(msg)

# Add a new staff member
class Staff(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    job_title: str
    salary: float

# Generate a random username and password
def generate_credentials(firstname,lastname):
    username = f"{firstname[:2]}{lastname[:2]}{random.randint(20, 70)}"
    password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return username, password

@app.post('/add_staff')
async def add_staff(staff: Staff):
    # Check if the email already exists
    existing_staff = await users_collection.find_one({'email': staff.email})
    if existing_staff:
        raise HTTPException(status_code=400, detail='Staff member already exists')

    # Generate the credentials
    firstname = staff.first_name
    lastname = staff.last_name
    username, password = generate_credentials(firstname,lastname)
    hashed_password = hash_password(password)

    # Save the staff member to the database
    await users_collection.insert_one({
        'first_name': staff.first_name,
        'last_name': staff.last_name,
        'email': staff.email,
        'phone_number': staff.phone_number,
        'job_title': staff.job_title,
        'salary': staff.salary,
        'username': username,
        'password': hashed_password
    })

    # Send the email
    send_email(staff.email, username, password)

    return {'message': 'Staff member added successfully ' + (password)}
    
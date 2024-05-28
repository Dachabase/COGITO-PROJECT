from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from pymongo import MongoClient
import random
import string

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["staff_db"]
staff_collection = db["staff"]

# Function to generate a random password
def generate_password(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# Function to check if staff exists in MongoDB
async def check_staff(first_name, last_name,job_title):
    staff = staff_collection.find_one({"first_name": first_name, "last_name": last_name, "job_title":job_title})
    if staff:
        return staff
    else:
        return None

# Function to create a new staff document in MongoDB
# async def create_staff(first_name, last_name, number, username, password):
#     staff = {
#         "first_name": first_name,
#         "last_name": last_name,
#         "number": number,
#         "username": username,
#         "password": password
#     }
#     staff_collection.insert_one(staff)

# API endpoint for stage 1: input first name, last name, and number
@app.post("/staff/login/step1")
async def login_step1(first_name: str, last_name: str, job_title: str):
    staff = await check_staff(first_name, last_name, job_title)
    if staff:
        return JSONResponse(content={"message": "Staff already exists"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Proceed to step 2"}, status_code=200)

# API endpoint for stage 2: generate username and password
@app.post("/staff/login/step2")
async def login_step2(first_name: str, last_name: str, number: int):
    staff = await check_staff(first_name, last_name, number)
    if staff:
        raise HTTPException(status_code=400, detail="Staff already exists")
    else:
        username = first_name[0] + last_name + str(number)
        password = generate_password(10)
        await create_staff(first_name, last_name, number, username, password)
        return JSONResponse(content={"username": username, "password": password}, status_code=201)
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import motor.motor_asyncio as aiomotor
from passlib.hash import bcrypt
import datetime

app = FastAPI()

client = aiomotor.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["mydatabase"]
users_collection = db["users"]

class User(BaseModel):
    name: str
    email: str
    password: str

@app.post("/signup/hr")
async def signup_hr(user: User):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hash(user.password)
    new_user = {"name": user.name, "email": user.email, "password": hashed_password, "role": "HR", "created_at": datetime.datetime.utcnow()}
    await users_collection.insert_one(new_user)

    return {"message": "User created successfully"}
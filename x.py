from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from passlib.hash import bcrypt
import motor.motor_asyncio as aiomotor
import jwt
from datetime import datetime, timedelta

app = FastAPI()

# Connect to MongoDB
client = aiomotor.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["mydatabase"]
users_collection = db["users"]

# Define the JWT secret key
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

# Define the OAuth2PasswordBearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define the User model
class User(BaseModel):
    username: str
    password: str
    role: str

# Define the Token model
class Token(BaseModel):
    access_token: str
    token_type: str

# Define the function to authenticate the user
async def authenticate_user(username: str, password: str):
    user = await users_collection.find_one({"username": username})
    if not user:
        return False
    if not bcrypt.verify(password, user["password"]):
        return False
    return user

# Define the function to generate the JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Define the login endpoint
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    authenticated_user = await authenticate_user(form_data.username, form_data.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": authenticated_user["username"], "role": authenticated_user["role"]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Define the protected endpoint for HR
@app.get("/hr")
async def hr(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role != "HR":
            raise HTTPException(status_code=403, detail="Forbidden")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return {"message": "Welcome to the HR page"}

# Define the protected endpoint for staff
@app.get("/staff")
async def staff(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role != "staff":
            raise HTTPException(status_code=403, detail="Forbidden")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return {"message": "Welcome to the staff page"}
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from database import users_collection

load_dotenv(dotenv_path="../.env")

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register(user: RegisterUser):
    existing_user = users_collection.find_one({"email": user.email})

    if existing_user:
        return {
            "success": False,
            "message": "Email already registered"
        }

    hashed_password = pwd_context.hash(user.password)

    users_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    })

    return {
        "success": True,
        "message": "User registered successfully"
    }


@router.post("/login")
def login(user: LoginUser):
    db_user = users_collection.find_one({"email": user.email})

    if not db_user:
        return {
            "success": False,
            "message": "Invalid email or password"
        }

    if not pwd_context.verify(user.password, db_user["password"]):
        return {
            "success": False,
            "message": "Invalid email or password"
        }

    token = create_token({
        "email": db_user["email"],
        "name": db_user["name"]
    })

    return {
        "success": True,
        "message": "Login successful",
        "token": token,
        "user": {
            "name": db_user["name"],
            "email": db_user["email"]
        }
    }
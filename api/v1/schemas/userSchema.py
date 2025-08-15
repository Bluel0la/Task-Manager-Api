from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserSignup(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    username: str
    password: str  # plaintext for signup only


class UserSignupResponse(BaseModel):
    id: str  # Firestore doc IDs are strings
    email: EmailStr
    firstname: str
    lastname: str
    username: str
    role: str
    created_at: datetime


class UserSignin(BaseModel):
    email: EmailStr
    password: str


class UserSigninResponse(BaseModel):
    id: str
    email: EmailStr
    firstname: str
    lastname: str
    username: str
    role: str
    created_at: datetime
    access_token: str  # Optional if using JWT or Firebase Auth

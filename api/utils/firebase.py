from firebase_admin import credentials, firestore
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime
import firebase_admin
import os

load_dotenv(".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Initialize Firebase Admin SDK

cred = credentials.Certificate(
    "api/utils/task-manager-blue-firebase-adminsdk-fbsvc-72b0a79e17.json"
)
firebase_admin.initialize_app(cred)

db = firestore.client()

# ------------------------
# CREATE USER (SIGNUP)
# ------------------------


def create_user(user_data):
    user_dict = user_data.dict()
    user_dict["password_hash"] = hash_password(user_dict.pop("password"))
    user_dict["created_at"] = datetime.utcnow()

    # Create document in Firestore
    user_ref = db.collection("users").document()  # auto-generate ID
    user_ref.set(user_dict)

    return {"id": user_ref.id, **user_dict}


# ------------------------
# GET USER BY EMAIL
# ------------------------
def get_user_by_email(email: str):
    users = db.collection("users").where("email", "==", email).limit(1).stream()
    user_doc = next(users, None)
    if not user_doc:
        return None
    user_data = user_doc.to_dict() or {}
    return {"id": user_doc.id, **user_data}


# ------------------------
# GET USER BY ID
# ------------------------
def get_user_by_id(user_id: str):
    doc = db.collection("users").document(user_id).get()
    if not doc.exists:
        return None
    user_data = doc.to_dict() or {}
    return {"id": doc.id, **user_data}

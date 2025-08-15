from api.v1.schemas.projectSchema import ProjectResponse, ProjectCreate
from firebase_admin import credentials, firestore
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime
import firebase_admin
import os, json

load_dotenv(".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Initialize Firebase Admin SDK

cred = credentials.Certificate(
    "etc/secrets/task-manager-blue-firebase-adminsdk-fbsvc-72b0a79e17.json"
)
#firebase_creds = json.loads(os.environ["FIREBASE_CREDENTIALS"])
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


# ------------------------
# Create Project
# ------------------------
def create_project(project_in: ProjectCreate, owner_username: str):
    # Ensure unique name
    if get_project_by_name(project_in.name):
        return None  # Caller will handle the error

    project_data = {
        "name": project_in.name.lower(),
        "description": project_in.description,
        "owner_username": owner_username,
        "created_at": datetime.utcnow(),
    }

    project_ref = db.collection("projects").document()
    project_ref.set(project_data)

    return ProjectResponse(
        id=project_ref.id,
        name=project_data["name"],
        description=project_data["description"],
        owner_username=project_data["owner_username"],
        created_at=project_data["created_at"],
    )


# ------------------------
# Get Project by ID
# ------------------------
def get_project_by_id(project_id: str):
    doc = db.collection("projects").document(project_id).get()
    if not doc.exists:
        return None
    return {"id": doc.id, **(doc.to_dict() or {})}


# ------------------------
# Get Project by Name
# ------------------------
def get_project_by_name(name: str):
    projects = (
        db.collection("projects").where("name", "==", name.lower()).limit(1).stream()
    )
    project_doc = next(projects, None)
    if not project_doc:
        return None
    data = project_doc.to_dict() or {}
    return ProjectResponse(
        id=project_doc.id,
        name=data["name"],
        description=data.get("description"),
        owner_username=data["owner_username"],
        created_at=data["created_at"],
    )


# ------------------------
# Get All Projects
# ------------------------
def get_all_projects():
    docs = db.collection("projects").stream()
    return [{"id": doc.id, **(doc.to_dict() or {})} for doc in docs]

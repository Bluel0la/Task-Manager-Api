import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(
    "task-manager-blue-firebase-adminsdk-fbsvc-72b0a79e17.json"
)
firebase_admin.initialize_app(cred)

db = firestore.client()

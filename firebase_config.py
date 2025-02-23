import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

# Replace with your actual Firebase configuration values
firebaseConfig = {
    "apiKey": "AIzaSyBTlRbjVXgosk9RM9JLQpUtJhhoeuwGDvM",
    "authDomain": "ai-powered-mock-interview-app.firebaseapp.com",
    "databaseURL": "",
    "projectId": "ai-powered-mock-interview-app",
    "storageBucket": "ai-powered-mock-interview-app.firebasestorage.app",
    "messagingSenderId": "1014856619225",
    "appId": "1:1014856619225:web:32651c32c2a9a11fc41ac8"
}

# Initialize Pyrebase for client-side authentication
firebase = pyrebase.initialize_app(firebaseConfig)
pb_auth = firebase.auth()

# Initialize Firebase Admin for Firestore
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
fs_client = firestore.client()

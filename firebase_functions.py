from firebase_admin import credentials, db, initialize_app

# Initialize Firebase app
cred = credentials.Certificate("firebase-creds-pyjamas.json")
initialize_app(
    cred,
    {
        "databaseURL": "https://pyjamas-4e19d-default-rtdb.asia-southeast1.firebasedatabase.app",
    },
)

from firebase_admin import firestore, credentials
import firebase_admin

from utility.constants import FIREBASE_SERVICE_ACCOUNT_PATH

# Use a service account
cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
defaul_app = firebase_admin.initialize_app(cred)

db = firestore.client()


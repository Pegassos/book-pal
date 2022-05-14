from firebase_admin import firestore, credentials
import firebase_admin

from utility.constants import FIREBASE_SERVICE_ACCOUNT_PATH

# Use a service account
cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
defaul_app = firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------------------------------------------
def initialize_book_doc(ref, favoriteCount = 0, readCount = 0, readingCount = 0):
  """Set book initial attributes if doc doesnt exist"""
  book_doc = ref.get()
  
  if not book_doc.exists:
    book_fields = {
      u'favoriteCount': favoriteCount,
      u'readCount': readCount,
      u'readingCount': readingCount
    }
    ref.set(book_fields)

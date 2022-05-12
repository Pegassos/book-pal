from fastapi import APIRouter, Depends, HTTPException
from lib.firebase import db
from firebase_admin import firestore 

from ..models.review import ReviewModel
from utility.utils import handle_exception
from lib.dependencies import get_current_user

# APIRouter creates path operations for review module
router = APIRouter(
  prefix = '/review',
  tags = ['Reviews'],
  responses={404: {"description": "Not found"}},
)

@router.get('/')
async def root():
  return {'Review -- index'}

@router.post('/create')
async def create_review(review: ReviewModel, user:str = Depends(get_current_user)):
  uid = user['uid']

  review_data = {
    u'uid': uid,
    u'isbn': review.isbn,
    u'content': review.content,
    u'createdAt': firestore.SERVER_TIMESTAMP
  }

  book_fields = {
    u'favoriteCount': 0,
    u'isRead': 0,
    u'isReading': 0
  }

  # Set user review subCollection
  user_ref = db.collection(u'users').document(uid).collection(u'reviews').document()
  user_ref.set(review_data)

  # Set book initial fields
  book_ref = db.collection(u'books').document(review.isbn)
  book_ref.set(book_fields)
  # Set book review subCollection
  book_ref.collection(u'reviews').document(user_ref.id).set(review_data)

  return {
    'uid': uid, 
    'review': review,
    # 'user_ref': user_ref.to_dict(),
    # 'book_ref': book_ref.to_dict(),
  }
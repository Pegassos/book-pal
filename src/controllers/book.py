from fastapi import APIRouter
from lib.firebase import db

# APIRouter creates path operations for user module
router = APIRouter(
  prefix = '/book',
  tags = ['Books'],
  responses = {404: {"description": "Not found"}},
)

@router.get('/')
async def root():
  return {'Index -- Books'}

@router.get('/reviews/{isbn}')
async def get_reviews(isbn: str):
  # Get reviews ref for book with isbn
  ref = db.collection(u'books').document(isbn).collection(u'reviews')
  docs = ref.get()

  # Get all reviews for the book
  reviews = {doc.id: doc.to_dict() for doc in docs}
  
  return {'r': reviews}
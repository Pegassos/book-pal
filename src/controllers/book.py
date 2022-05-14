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

@router.get('/{isbn}')
async def get_book(isbn: str):
  # Book attributes
  book_ref = db.collection(u'books').document(isbn)
  book_doc = book_ref.get()

  # Book reviews
  reviews_ref = book_ref.collection(u'reviews')
  reviews_docs = reviews_ref.get()
  # Get all reviews for the book
  reviews = {doc.id: doc.to_dict() for doc in reviews_docs}

  return {
    'isbn': isbn,
    'data': book_doc.to_dict(),
    'reviews': reviews
  }

# @router.get('/reviews/{isbn}')
# async def get_reviews(isbn: str):
#   # Get reviews ref for book with isbn
#   ref = db.collection(u'books').document(isbn).collection(u'reviews')
#   docs = ref.get()

#   # Get all reviews for the book
#   reviews = {doc.id: doc.to_dict() for doc in docs}
  
#   return {'reviews': reviews}
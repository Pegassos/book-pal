import pickle
from fastapi import APIRouter
from lib.firebase import db
from src.models.book import IsbnArrayModel
from utility.utils import get_recommendations

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

  # Get Reviews
  reviews_ref = book_ref.collection(u'reviews')
  # Get all reviews for the book oredered by createdat
  reviews_docs = reviews_ref.order_by(u'createdAt').get()
  reviews = [doc.to_dict() for doc in reviews_docs]

  # Get Recommendations
  pickle_data = pickle.load(open('lib/pickle_data', 'rb'))
  pickle_model = pickle.load(open('lib/pickle_model', 'rb'))
  recommendations = get_recommendations(isbn, pickle_data, pickle_model)

  return {
    'isbn': isbn,
    'data': book_doc.to_dict(),
    'reviews': reviews,
    'recommendations': recommendations
  }

@router.get('/array/get')
async def get_recommendation_for_array(isbnArray: IsbnArrayModel):
  # Get Recommendations
  pickle_data = pickle.load(open('lib/pickle_data', 'rb'))
  pickle_model = pickle.load(open('lib/pickle_model', 'rb'))

  recommendations = []
  for isbn in isbnArray.items:
    rcm = get_recommendations(isbn, pickle_data, pickle_model)
    for id in rcm:
      recommendations.append(id)

  unique_set_recommendation = set(recommendations)
  
  return {
    'isbnArray': isbnArray,
    'recommendations': unique_set_recommendation
  }

# @router.get('/reviews/{isbn}')
# async def get_reviews(isbn: str):
#   # Get reviews ref for book with isbn
#   ref = db.collection(u'books').document(isbn).collection(u'reviews')
#   docs = ref.get()

#   # Get all reviews for the book
#   reviews = {doc.id: doc.to_dict() for doc in docs}
  
#   return {'reviews': reviews}
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
async def root(search: str):
  """
    search: search input from user
    search in BOOKS for books containing search string and return isbn array
  """
  pickle_data = pickle.load(open('lib/pickle_data', 'rb'))
  BOOK_PIVOT, BOOK_ISBN_LIST, BOOKS = pickle_data
  
  # get isbn for books whom title contains search string 
  array = BOOKS[BOOKS['title'].str.contains(search)]['ISBN'].to_dict()
  result = [isbn for isbn in array.values()]

  # filter result for isbn in BOOK_ISBN_LIST
  for isbn in result:
    if not isbn in BOOK_ISBN_LIST:
      result.remove(isbn)
  
  return {
    'search': search,
    "length": len(result),
    'data': result,
  }



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

@router.post('/array/get')
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

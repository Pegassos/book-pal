from enum import Enum
from typing import Optional
from fastapi import HTTPException

class Gender(str, Enum):
  MALE = 'male'
  FEMALE = 'female'

def handle_exception(e: Exception, status_code: Optional[int] = 400):
  detail = {
    'exception': e.__class__.__name__,
    'code': e.code if hasattr(e, 'code') else None,
    'message': e.default_message if hasattr(e, 'default_message') else str(e),
  }
  
  raise HTTPException(status_code=status_code, detail=detail)

def get_index_by_isbn(BOOK_ISBN_LIST, BOOK_ISBN):
  FIRST_MATCHING_ISBN = [isbn for isbn in BOOK_ISBN_LIST if BOOK_ISBN == isbn][0]
  return BOOK_ISBN_LIST.index(FIRST_MATCHING_ISBN)

def get_title_by_isbn(BOOKS, ISBN):
  return BOOKS.loc[BOOKS['ISBN'] == ISBN]['title'].tolist()[0]


def get_recommendations(isbn, pickle_data, pickle_model):
  # Load data & model
  BOOK_PIVOT, BOOK_ISBN_LIST, BOOKS = pickle_data
  model = pickle_model

  try:
    INDEX_SUGGESTION = get_index_by_isbn(BOOK_ISBN_LIST, isbn)
  except IndexError:
    return {
      "exception": 'IndexError',
      'detail': {
        "isbn": isbn,
        "error": "Book not found"
      }
    }

  recommendations = model.kneighbors(BOOK_PIVOT.iloc[INDEX_SUGGESTION, :].values.reshape(1, -1))[1][0].tolist()
  # print(recommendations)

  # Fill books array with {id, title} dict 
  return [BOOK_PIVOT.index[id] for id in recommendations]

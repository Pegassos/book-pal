from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from firebase_admin import firestore 

class ReviewModel(BaseModel):
  isbn: str = Field(description = 'Book isbn, book concerned about the review')
  content: str = Field(description = 'Content of the review')
  # UID & createdAt are auto generated
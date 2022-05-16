# Book should be just ISBN
# Models for get recommendations bulk

from pydantic import BaseModel, Field

class IsbnArrayModel(BaseModel):
  items: list = Field(description = 'Array of books')
from pydantic import BaseModel, Field

class FavoriteModel(BaseModel):
  isbn: str = Field(description = 'Book isbn, book to add/remove to favorites')
  # toggleFavorite: bool = Field(description = 'Boolean to toggle favorite status')
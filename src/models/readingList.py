from typing import Optional
from pydantic import BaseModel, Field

class ManageReadingListModel(BaseModel):
  isbn: str = Field(description = 'Book isbn, book to add/remove from lists')
  isRead: bool = Field(description = 'Boolean to add_to/remove_from book currently_reading/already_red lists')
  currentIsRead: Optional[bool] = Field(None, description = 'Used in List state update')
  delete: Optional[bool] = Field(None, description = 'If True: remove book from both lists') 
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from utility.utils import Gender

class EditUserModel(BaseModel):
  email: Optional[str] = Field(None, description = 'User email')
  password: Optional[str] = Field(None, description = 'User password')
  firstName: Optional[str] = Field(None, description = 'User firstname')
  lastName: Optional[str] = Field(None, description = 'User lastname')
  displayName: Optional[str] = Field(None, description = 'User display name')
  birthday: Optional[datetime] = Field(None, description = 'User birthday')
  gender: Optional[Gender] = Field(None, description = 'User gender')
  photoURL: Optional[str] = Field(None, description = 'Profile image as str url')

class CreateUserModel(BaseModel):
  email: str
  password: str
  firstName: str
  lastName: str
  birthday: datetime
  gender: Gender
  photoURL: Optional[str] = Field(None, description='Profile image as str url')

  # def is_valid(self):
    # user = auth.get_user_by_email(self.email)
    
    # return False if user else True
    # if user:
    #   return False
    #   # raise HTTPException(status_code=401, detail="Email is taken")
    # return True
  
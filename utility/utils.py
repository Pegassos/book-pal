from asyncio.windows_events import NULL
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
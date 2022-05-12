from fastapi import Header, HTTPException, Depends
from firebase_admin import auth

from utility.utils import handle_exception

async def parse_token(authorization: str = Header(...)):
  """Get Authorization header with Bearer token from headers"""
  token = authorization.split(' ')[1]
  # if not token:
  #   raise HTTPException(status_code=400, detail="Authorization header missing")
  return token

async def get_current_user(token: str = Depends(parse_token)):
  """Verify the token with firebase auth"""
  try:
    user = auth.verify_id_token(token)
  except Exception as e:
    handle_exception(e, status_code=401)

  return user
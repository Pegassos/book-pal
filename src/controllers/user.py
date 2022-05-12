from fastapi import APIRouter, Depends, Query, HTTPException
from firebase_admin import auth
from lib.firebase import db

from ..models.user import EditUserModel, CreateUserModel
from utility.utils import handle_exception
from lib.dependencies import get_current_user

# APIRouter creates path operations for user module
router = APIRouter(
  prefix = '/user',
  tags = ['User'],
  responses={404: {"description": "Not found"}},
)

@router.get('/')
async def root():
  return {'index -- User'}

@router.get('/{uid}')
async def get_user(uid: str):
  try:
    user = auth.get_user(uid)
  except Exception as e:
    handle_exception(e)
  
  return user

@router.post('/create')
async def create_user(user: CreateUserModel):
  """Create new user in Firebase"""
   
  try:
    # Create new user in Athentication
    created_user = auth.create_user(
      email = user.email,
      # email_verified=False,
      password = user.password,
      # display_name='Create User 1',
      disabled=False
    )

    uid = created_user.uid

    # Create new user in Firestore with uid
    user_data = {
      u'firstName': user.firstName,
      u'lastName': user.lastName,
      u'birthday': user.birthday,
      u'photoUrl': user.photoURL,
      u'gender': user.gender
    }
    user_ref = db.collection(u'users').document(uid).set(user_data)
    # user.ref
  
  except Exception as e:
    handle_exception(e)

  return {'user': user, 'created_user': created_user, 'uid': uid}

@router.put('/edit')
async def edit_user(user: EditUserModel, current_user: str = Depends(get_current_user)):
  """Update user profile"""
  uid = current_user['uid']
  
  # Edit user in Firestore
  user_ref = db.collection(u'users').document(uid) 
  if user_ref.get().exists:
    # Edit user doc
    user_ref.update({
      u'firstName': user.firstName,
      u'lastName': user.lastName,
      u'birthday': user.birthday,
      u'photoUrl': user.photoURL,
      u'gender': user.gender
    })
  else:
    # Create user doc
    user_data = {
      u'firstName': user.firstName,
      u'lastName': user.lastName,
      u'birthday': user.birthday,
      u'photoUrl': user.photoURL,
      u'gender': user.gender
    }
    user_ref = db.collection(u'users').document(uid).set(user_data)

  # user_doc = user_doc_ref.get()
  # if user_doc.exists:
  #   print('----------------ecxists----------------')
  # else:
  #   raise HTTPException(status_code=404, detail='User document doesnt exist. Please contact the admin')

  # Edit user in Authentication
  try:
    user_update = auth.update_user(
      uid = uid,
      email = user.email,
      # email_verified = True,
      password = user.password,
      display_name = user.displayName,
      photo_url = user.photoURL,
      # disabled=True
    )
  except Exception as e:
    handle_exception(e)

  return {
    'user': user,
    'userUpdate': user_update,
    'uid': current_user['uid']
  }
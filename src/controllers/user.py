from fastapi import APIRouter, Depends, Query, HTTPException
from firebase_admin import auth, firestore
from pandas import array


from ..models.user import EditUserModel, CreateUserModel
from src.models.favorite import FavoriteModel
from src.models.readingList import readingListsData
from utility.utils import handle_exception
from lib.firebase import db, initialize_book_doc
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
    user_ref = db.collection(u'users').document(uid)
    user_data = {
      u'firstName': user.firstName,
      u'lastName': user.lastName,
      u'birthday': user.birthday,
      u'photoUrl': user.photoURL,
      u'gender': user.gender,
      u'favorites': []
    }
    user_ref.set(user_data)
  
  except Exception as e:
    handle_exception(e)

  return {'user': user, 'created_user': created_user, 'uid': uid}

@router.put('/edit')
async def edit_profile(user: EditUserModel, current_user: str = Depends(get_current_user)):
  """Update user profile"""
  uid = current_user['uid']

  # Get fields to update from user edit model
  data = get_edit_profile_fields(user)
  
  # Edit user in Firestore
  user_ref = db.collection(u'users').document(uid) 
  if len(data['user_doc']) > 0:
    if user_ref.get().exists:
      # Edit user doc
      user_ref.update(data['user_doc'])
      # user_ref.update({
      #   u'firstName': user.firstName,
      #   u'lastName': user.lastName,
      #   u'birthday': user.birthday,
      #   u'photoUrl': user.photoURL,
      #   u'gender': user.gender
      # })
    else:
      # Create user doc - wont reach this point cause user ref always exists since sign up
      # user_data = {
      #   u'firstName': user.firstName,
      #   u'lastName': user.lastName,
      #   u'birthday': user.birthday,
      #   u'photoUrl': user.photoURL,
      #   u'gender': user.gender
      # }
      user_ref = db.collection(u'users').document(uid).set(data['user_doc'])

  # Edit user in Authentication
  if len(data['user_auth']):
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
    # 'userUpdate': user_update,
    'uid': current_user['uid']
  }

@router.post('/toggleFavorite')
async def toggle_favorite(favorite: FavoriteModel, user: str = Depends(get_current_user)):
  uid = user['uid']
  isbn = favorite.isbn

  # Do batch writes
  batch = db.batch()

  # User  ----------------------------
  # favoriteCount is an Array field - Add/Remove isbn from the array
  user_ref = db.collection('users').document(uid)

  # Check if book is already in the array
  book_is_favorite = user_ref.get().to_dict()['favoriteCount'].__contains__(isbn)
  # Calculate value for firestore method (increment +1, decrement -1) - Used in book update below
  count = -1 if book_is_favorite else 1
  
  # Update user data
  user_data = {
    u'favoriteCount': firestore.ArrayRemove([isbn]) if book_is_favorite else firestore.ArrayUnion([isbn])
  }
  batch.update(user_ref, user_data)

  # Book  ----------------------------
  book_ref = db.collection(u'books').document(isbn)
  # initialize doc if not exist
  initialize_book_doc(book_ref)

  # update book data
  data = {
    u'favoriteCount': firestore.Increment(count)
  }
  batch.update(book_ref, data)


  batch.commit()

  return {
    'uid': uid,
    'isbn': isbn,
    'book_state': 'Removed book from favorites' if book_is_favorite else 'Added book to favorites'
  }

@router.post('/manageReadingLists')
async def manage_reading_lists(data: readingListsData, user: str = Depends(get_current_user)):
  uid = user['uid']
  isbn = data.isbn
  isRead = data.isRead

  # user data 
  user_data = {
    u'isbn': isbn,
    u'isRead': isRead
  }
  # book data
  # For init book doc if necessary
  readCount = 1 if isRead else 0
  readingCount = 0 if isRead else 1
  book_data = {
    u'readCount': firestore.Increment(readCount),
    u'readingCount': firestore.Increment(readingCount)
  }
  # still need to handle counters when removing book from lists

  batch = db.batch()

  # User ---------------------------
  user_ref = db.collection(u'users').document(uid).collection(u'readingLists')
  user_lists_ref = user_ref.document(isbn)
  # Book ---------------------------
  book_ref = db.collection(u'books').document(isbn)
  # Initi book doc if not exist
  initialize_book_doc(book_ref, readCount=readCount, readingCount=readingCount)

  if user_lists_ref.get().exists:
    if data.removerFromLists:
      # Delete doc from collection
      batch.delete(user_lists_ref)
    else:
      # Update doc in user
      batch.update(user_lists_ref, user_data)
      # Increment/Decrement counters in book
      batch.update(book_ref, book_data)
  else:
    # Set user doc
    batch.set(user_lists_ref, user_data)
    # Increment/Decrement counters in book
    batch.update(book_ref, book_data)
  
  # Commit changes to db
  batch.commit()  
  
  return {
    'uid': uid,
    'data': data
  }



# Helper functions ------------------ 
def get_edit_profile_fields(user: EditUserModel):
  # user doc fields ----------------------
  user_doc = {
    u'firstName': user.firstName,
    u'lastName': user.lastName,
    # u'birthday': user.birthday,
    u'photoUrl': user.photoURL,
    # u'gender': user.gender
  }
  # if user.firstName:
  #   user_doc[u'firstName'] = user.firstName

  # if user.lastName:
  #   user_doc[u'lastName'] = user.lastName

  # if user.birthday:
  #   user_doc[u'birthday'] = user.birthday

  # if user.gender:
  #   user_doc[u'gender'] = user.gender

  # if user.photoURL:
  #   user_doc[u'photoURL'] = user.photoURL

  # user auth fields --------------------
  user_auth = {}
  # if user.email:
  #   user_auth[u'email'] = user.email

  # if user.password:
  #   user_auth[u'password'] = user.password

  # if user.displayName:
  #   user_auth[u'displayName'] = user.displayName

  return {
    'user_doc': user_doc, 
    'user_auth': user_auth
  }
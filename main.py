from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.api import router as api_router
from utility.constants import ORIGINS
from lib.firebase import defaul_app

# Init FastApi server
app = FastAPI()

# Init Firebase default app
# cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
# default_app = firebase_admin.initialize_app(cred)

app.add_middleware(
  CORSMiddleware,
  allow_origins = ORIGINS,
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ["*"],
)

app.include_router(api_router)
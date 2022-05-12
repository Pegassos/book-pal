from fastapi import APIRouter
from src.controllers import user, book, review

router = APIRouter()

router.include_router(review.router)
router.include_router(user.router)
router.include_router(book.router)
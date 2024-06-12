from .todos import todos
from .auth import auth_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(todos, prefix='/todos')
router.include_router(auth_router, prefix='/saml2')

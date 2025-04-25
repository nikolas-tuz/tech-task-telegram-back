from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.params import Depends

from decorators.auth_guard import auth_guard

router = APIRouter(prefix="/telegram")

load_dotenv()


@router.get('/')
async def health_check(user: dict = Depends(auth_guard)):
    return {"message": "/telegram is healthy."}

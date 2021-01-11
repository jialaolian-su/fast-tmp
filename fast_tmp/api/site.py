from fastapi import APIRouter

from fast_tmp.depends import get_current_user

router = APIRouter(prefix="/base")

from fastapi import Depends, Response, Cookie
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.main_app import application as app
from app.cookie import *
from app.main_app import get_db


@app.get("/personal_area")
async def a(cookie_token: Optional[str] = Cookie(default=None),  db: Session = Depends(get_db)):
    """Переадресация на страницу документации"""
    if check_cookie_for_validity(db=db, cookie_token=cookie_token):
        return Response("Вы авторизированы", media_type="text/html")
    return RedirectResponse('/')
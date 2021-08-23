from fastapi import Depends, Response, Form, Cookie
from sqlalchemy.orm import Session
from fastapi import Request
from fastapi.templating import Jinja2Templates
from app.main_app import application as app
from app.cookie import *
from app.main_app import get_db
import json


templates = Jinja2Templates(directory="./tmp/")


@app.get("/registration")
async def authorization(request: Request) -> templates:
    """
    Страница с формой регистрации

    :param request:
    :return: Возвращает html/login.html
    """
    return templates.TemplateResponse("html/registration.html", {"request": request})


@app.post("/registration_user")
async def process_login_page(db: Session = Depends(get_db),
                             username: str = Form(...),
                             password: str = Form(...),
                             cookie_token: Optional[str] = Cookie(default=None)) -> Response:
    """
    Принимает на вход username и password.
    Возвращает {"success": True} при успешной регистрации иначе {"success": False}

    :param db: Соединение с базой данных
    :param username: str
    :param password: str
    :param cookie_token: Optional[str]
    :return: Response
    """
    if cookie_token:
        Response().delete_cookie(key="cookie_token")
    if crud.get_user_by_username(db=db, username=username) == username:
        return Response(json.dumps({"success": "Such a user already exists"}), media_type="application/json")
    if cookie_token := create_new_cookie_token(username=username, password=password):
        if password_hash := get_username_from_signed_string(cookie_token=cookie_token):
            if crud.create_new_user(db=db, username=username, hashed_password=password_hash[1]):
                response = Response(json.dumps({"success": True}), media_type="application/json")
                response.set_cookie(key="cookie_token", value=cookie_token)
                return response
    return Response(json.dumps({"success": False}), media_type="application/json")
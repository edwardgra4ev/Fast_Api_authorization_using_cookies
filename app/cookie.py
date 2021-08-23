import hashlib
import hmac
import base64
import binascii
from typing import Optional
import sql_app.sql_queries as crud


SECRET_KEY = "c1d8d450bb23321ed96939d058d4dce02568c0a72a710151b00d43eb1b96f4fe"


def create_new_cookie_token(username: str, password: str) -> Optional[str]:
    """
    Функция создания токена cookie для цифровой подписи
    :param username: str
    :param password: str
    :return: Возвращает cookie_token если login и password переданны корректно. Иначе None
    """
    if isinstance(username, str) and isinstance(password, str):
        hash = hmac.new(
            SECRET_KEY.encode(),
            msg=password.encode(),
            digestmod=hashlib.sha256
        ).hexdigest().upper()
        cookie_token = f"{base64.b64encode(username.encode()).decode()}.{hash}"
        return cookie_token


def get_username_from_signed_string(cookie_token: str) -> Optional[tuple]:
    """
    Функция парсит cookie_token и преобразовывает в номрмальный username и password_hash
    :param cookie_token: str
    :return: tuple(username: str, password_hash: str)
    """
    try:
        username_base64, password_hash = cookie_token.split('.')
        username = base64.b64decode(username_base64).decode("utf-8")
        return username, password_hash
    except ValueError:
        return None
    except binascii.Error:
        return None


def check_cookie_for_validity(db, cookie_token: str) -> bool:
    """
    Функция проверяет пришли ли cookie валидного пользователя
    :param db: Соезденение с базой данных
    :param cookie_token: str
    :return:
    """
    if cookie_token_parsed := get_username_from_signed_string(cookie_token):
        username, password_hash = cookie_token_parsed
        return crud.check_if_there_is_username_and_password(db=db, username=username, hashed_password=password_hash)
    return False

from sqlalchemy.orm import Session
from sql_app import models
from typing import Optional


def check_if_there_is_username_and_password(db: Session, username: str, hashed_password: str) -> bool:
    """
    Проверяет еслть ли пользователь с таким username и hashed_password в бд

    :param db: Session
    :param username: str
    :param hashed_password: str
    :return: bool
    """
    if db.query(models.User).filter(models.User.username == username,
                                    models.User.hashed_password == hashed_password).first():
        return True
    return False


def get_user_by_username(db: Session, username: str) -> Optional[str]:
    """
    Возращает логин пользователя если он есть в бд
    
    :param db: Session
    :param username: str
    :return: Optional[str]
    """
    if query := db.query(models.User).filter(models.User.username == username).first():
        return query.username


def create_new_user(db: Session, username: str, hashed_password: str) -> bool:
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True



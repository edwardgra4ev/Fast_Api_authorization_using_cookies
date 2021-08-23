from fastapi import FastAPI
from sql_app.database import SessionLocal, engine
from sql_app import models

# Инициализация FastApi
application = FastAPI(
    title="Test project on FastAPI",
    description="Тестовый проект с использованием FastAPI",
    version="0.1.0",

)

models.Base.metadata.create_all(bind=engine)


# Соединение с бд
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
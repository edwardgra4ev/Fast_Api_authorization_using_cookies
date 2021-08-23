from fastapi.responses import RedirectResponse
import uvicorn
from app.main_app import application as app


# Запуск программы
if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000)
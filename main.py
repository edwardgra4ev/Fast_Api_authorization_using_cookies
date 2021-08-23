from fastapi.responses import RedirectResponse
import uvicorn
from app.main_app import application as app


# Запуск программы
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
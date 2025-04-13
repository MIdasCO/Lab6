from fastapi import FastAPI
from app.database import engine, Base
from app.routes.auth_routes import router as auth_routes_router
from app.routes.user_routes import router as user_routes_router
import uvicorn
from app.database import engine, Base
import app.models  # чтобы модели были зарегистрированы

Base.metadata.create_all(bind=engine)


app = FastAPI(title="FastAPI + DB for User Interactions")

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Подключаем маршруты
app.include_router(auth_routes_router, prefix="/auth", tags=["auth"])
app.include_router(user_routes_router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

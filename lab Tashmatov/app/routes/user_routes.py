from fastapi import APIRouter, Depends
from app import auth, schemas

router = APIRouter()

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user = Depends(auth.get_current_user)):
    return current_user

@router.get("/button")
def button_action(current_user = Depends(auth.get_current_user)):
    return {
        "message": f"Кнопка нажата пользователем {current_user.username} с ролью {current_user.role}"
    }

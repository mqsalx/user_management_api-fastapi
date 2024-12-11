# /app/routes/user_router.py

from fastapi import APIRouter, Depends

from api.controllers.user.user_controller import UserController
from dtos.user.user_dto import UserCreateDTO

router = APIRouter()


@router.post("/users/")
def create_user(
    user_data: UserCreateDTO,
    user_controller: UserController = Depends(UserController),
):
    return user_controller.create_user(user_data)


@router.get("/users/")
def get_users(user_controller: UserController = Depends(UserController)):
    return user_controller.get_users()


@router.get("/users/{user_id}")
def get_user(
    user_id: int, user_controller: UserController = Depends(UserController)
):
    return user_controller.get_user(user_id)

# /src/presentation/routes/user/__init__.py

# flake8: noqa: E501

# PY
from fastapi import APIRouter

# Presentation
from src.presentation.routes.user.create import CreateUserRouter
from src.presentation.routes.user.get import GetUserRouter
from src.presentation.routes.user.remove import RemoveUserRouter
from src.presentation.routes.user.update import UpdateUserRouter

user_router = APIRouter()


CreateUserRouter(user_router)
GetUserRouter(user_router)
RemoveUserRouter(user_router)
UpdateUserRouter(user_router)



# @user_router.get("", response_model=None)
# def get_users_or_get_by_user_id_router(
#     query_params: FindUserByUserIdDTO = Depends(),
#     session_db: Session = Depends(DatabaseConfig().get_db),
# ) -> JSONResponse:
#     """
#     Endpoint that retrieves user(s).

#     If a `user_id` is provided, it retrieves a specific user. Otherwise, it returns all users.

#     Args:
#         query_params:
#             user_id (str, optional): Unique identifier of the user to retrieve.
#                 If not provided, retrieves all users.
#         session_db (Session): Database session dependency, injected via FastAPI's Depends.

#     Returns:
#         JSONResponse: A JSON response containing user details.

#     Raises:
#         HTTPException: If no users are found.
#     """

#     controller = UserController(session_db)
#     return controller.find_user_controller(query_params)


# @user_router.patch("/{user_id}", response_model=None)
# def update_user_router(
#     user_id: str,
#     request: UpdateUserRequestDTO,
#     session_db: Session = Depends(DatabaseConfig().get_db),
# ) -> JSONResponse:
#     """
#     Endpoint that updates user information.

#     This Standalone Function updates the details of an existing user based on the provided user ID.

#     Args:
#         user_id (str): Unique identifier of the user to update.
#         request (UpdateUserRequestDTO): Data Transfer Object (DTO) containing
#             the updated user details (e.g., name, email, password).
#         session_db (Session): Database session dependency, injected via FastAPI's Depends.

#     Returns:
#         JSONResponse: A JSON response confirming the update.

#     Raises:
#         HTTPException: If the user is not found or update fails.
#     """

#     controller = UserController(session_db)
#     return controller.update_user_controller(user_id, request)

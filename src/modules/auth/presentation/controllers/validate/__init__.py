# /src/presentation/controllers/uth/verification/__init__.py

# flake8: noqa: E501

# PY
from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Callable

# Domain
from src.domain.use_cases import ValidateUseCase
from src.utils import ResponseUtil

response_json: Callable[..., JSONResponse] = ResponseUtil().json_response


class ValidateController:
    """
    Class Controller responsible for handling user authentication requests.

    This class provides an endpoint to authenticate users, validate credentials,
    and return an access token upon successful authentication.

    Class Args:
        session_db (Session): The database session used for executing queries.
    """

    def __init__(self) -> None:
        """
        Constructor method that initializes the LoginController with database dependencies.

        Args:
            session_db (Session): Database session dependency,
                injected via FastAPI's Depends.
        """
        self.__use_case = ValidateUseCase()

    def __call__(self, request: Request) -> JSONResponse:
        """
        Public method that authenticates a user based on the provided credentials.

        Args:
            request (Request): Data Transfer Object (DTO) containing
                the user's login credentials (e.g., email and password).

        Returns:
            JSONResponse: A JSON response containing an authentication token if successful.

        Raises:
            HTTPException: If authentication fails due to invalid credentials.
        """
        use_case_response = self.__use_case(request)


        status_code = status.HTTP_200_OK
        message = "Token is valid!"


        return response_json(
            status_code=status_code,
            message=message,
            data=use_case_response
        )

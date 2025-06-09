# /src/presentation/routes/auth/verification/__init__.py

# flake8: noqa: E501

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

# Presentation
from src.presentation.controllers import ValidateController


class ValidateRouter:
    """
    """
    def __init__(self, user_router: APIRouter) -> None:
        """
        """
        self.__router: APIRouter = user_router

        self.__router.get(
            path="/validate",
            description=""
        )(self.__call__)

    def __call__(
        self,
        request: Request = None
    ) -> JSONResponse:
        """
        Endpoint that handles user creation.

        This method processes user registration requests and returns
            a confirmation message upon successful user creation.
        """
        controller = ValidateController()
        return controller(request)

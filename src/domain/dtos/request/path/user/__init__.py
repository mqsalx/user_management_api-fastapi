# /src/domain/dtos/user/__init__.py

# flake8: noqa: E501

# Domain
from fastapi import Path
from src.domain.dtos.base import BaseDTO


class RemoveUserByUserIdReqPathDTO(BaseDTO):
    """
    Class responsible for the Data Transfer Object (DTO) for user creation.

    This class is responsible for validating and structuring user creation requests.
    """

    user_id: str


class UpdateUserReqPathDTO(BaseDTO):
    """
    Class responsible for the Data Transfer Object (DTO) for user update.

    This class is responsible for validating and structuring user update requests.
    """

    user_id: str

    @staticmethod
    def validate_path(user_id: str = Path(...)) -> "RemoveUserByUserIdReqPathDTO":
        """
        Static method to create an instance of RemoveUserByUserIdReqPathDTO from a FastAPI path parameter.

        Args:
            user_id (str): The user ID extracted from the path.

        Returns:
            RemoveUserByUserIdReqPathDTO: A validated DTO instance containing the user_id.
        """
        return RemoveUserByUserIdReqPathDTO(user_id=user_id)
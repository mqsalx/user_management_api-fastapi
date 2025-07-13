# /src/modules/user/presentation/schemas/request/path/__init__.py

# PY
from fastapi import Path

# Shared
from src.shared.presentation.schemas.base import BaseSchema


class RemoveUserByUserIdReqPathSchema(BaseSchema):
    """
    Class responsible for the Data Transfer Object (DTO) for user creation.

    This class is responsible for validating
        and structuring user creation requests.
    """

    user_id: str


class UpdateUserReqPathSchema(BaseSchema):
    """
    Class responsible for the Data Transfer Object (DTO) for user update.

    This class is responsible for validating
        and structuring user update requests.
    """

    user_id: str

    @staticmethod
    def validate_path(user_id: str = Path(...)) -> "UpdateUserReqPathSchema":
        """
        Static method to create an instance of UpdateUserReqPathSchema
            from a FastAPI path parameter.

        Args:
            user_id (str): The user ID extracted from the path.

        Returns:
            RemoveUserByUserIdReqPathDTO: A validated DTO instance
                containing the user_id.
        """
        return UpdateUserReqPathSchema(user_id=user_id)


class FindUserByUserIdPathSchema(BaseSchema):
    """ """

    user_id: str

    @staticmethod
    def validate_path(
        user_id: str = Path(...),
    ) -> "FindUserByUserIdPathSchema":
        """ """
        return FindUserByUserIdPathSchema(user_id=user_id)

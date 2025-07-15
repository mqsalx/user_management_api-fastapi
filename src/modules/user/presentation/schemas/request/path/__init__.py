# /src/modules/user/presentation/schemas/request/path/__init__.py

# PY
from fastapi import Path

# Shared
from src.shared.presentation.schemas.base import BaseSchema


class RemoveUserByUserIdReqPathReq(BaseSchema):
    """
    Class responsible for the Data Transfer Object (DTO) for user creation.

    This class is responsible for validating
        and structuring user creation requests.
    """

    user_id: str


class UpdateUserReqPathReq(BaseSchema):
    """
    Class responsible for the Data Transfer Object (DTO) for user update.

    This class is responsible for validating
        and structuring user update requests.
    """

    user_id: str

    @staticmethod
    def validate_path(user_id: str = Path(...)) -> "UpdateUserReqPathReq":
        """
        Static method to create an instance of UpdateUserReqPathReq
            from a FastAPI path parameter.

        Args:
            user_id (str): The user ID extracted from the path.

        Returns:
            RemoveUserByUserIdReqPathDTO: A validated DTO instance
                containing the user_id.
        """
        return UpdateUserReqPathReq(user_id=user_id)


class FindUserByUserIdPathReq(BaseSchema):
    """ """

    user_id: str

    @staticmethod
    def validate_path(
        user_id: str = Path(...),
    ) -> "FindUserByUserIdPathReq":
        """ """
        return FindUserByUserIdPathReq(user_id=user_id)

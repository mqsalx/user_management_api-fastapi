# /src/api/schemas/user/response/__init__.py

from src.api.schemas.base.response import BaseResponse


class UserResponse(BaseResponse):
    """
    Class representing the response schema for user-related operations.

    Inherits from `BaseResponse` and is used to structure responses
    returned from user endpoints, including status code, message,
    data, and optionally pagination or metadata.

    This class is typically used in controller or router layers
    to maintain consistency across user-related responses.
    """
    pass

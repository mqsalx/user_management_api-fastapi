# /src/domain/dtos/response/user/__init__.py

# flake8: noqa: E501

from pydantic import BaseModel

from typing import Dict, List, Union

from pydantic import RootModel


# class UserResponseSchema(RootModel):
#     """
#     Class responsible for the Data Transfer Object (DTO) for user-related responses.

#     This class structures responses for user-related API calls, returning user details
#     as a dictionary or a list of dictionaries.
#     """

#     root: Union[Dict[str, str], List[Dict[str, str]]]


class UserResponseSchema(BaseModel):
    """
    """

    user_id: str
    name: str
    email: str
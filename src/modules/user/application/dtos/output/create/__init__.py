# /src/modules/user/application/dtos/output/create/__init__.py

# PY
from dataclasses import dataclass

from src.modules.user.domain.entities import UserEntity


@dataclass
class CreateUserOutput:
    """
    Class representing the output DTO for the CreateUser use case.

    Represents the response structure returned after successfully creating a user.
    It contains basic identifying information about the newly created user.

    Class Args:
        user_id (str): The unique identifier of the created user.
        name (str): The name of the user.
        email (str): The email address of the user.
        status (str): The current status of the user (e.g., 'active').
        role_id (str): The role identifier associated with the user.
    """

    user_id: str
    name: str
    email: str
    status: str
    role_id: str

    @classmethod
    def format(cls, entity: UserEntity) -> "CreateUserOutput":
        """
        Class method that converts a UserEntity instance
            into a CreateUserOutput DTO.

        Args:
            entity (UserEntity): The user entity to be transformed.

        Returns:
            CreateUserOutput: A DTO populated with data from the given entity.
        """
        return cls(
            user_id=entity.user_id,
            name=entity.name,
            email=entity.email,
            status=entity.status,
            role_id=entity.role_id,
        )

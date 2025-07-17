# /src/modules/user/application/dtos/output/update/__init__.py

from dataclasses import dataclass

from src.modules.user.domain.entities import UserEntity


@dataclass(frozen=True)
class UpdateUserOutput:
    """
    Class representing the output DTO for the UpdateUser use case.

    Represents the response structure returned after
        a user is successfully updated.

    Class Args:
        user_id (str): The unique identifier of the updated user.
        name (str): The updated name of the user.
        email (str): The updated email address of the user.
        status (str): The updated status of the user (e.g., 'active').
        role_id (str): The role identifier currently assigned to the user.
    """
    user_id: str
    name: str
    email: str
    status: str
    role_id: str

    @classmethod
    def format(cls, entity: UserEntity) -> "UpdateUserOutput":
        """
        Class method that converts a UserEntity instance
            into an UpdateUserOutput DTO.

        Args:
            entity (UserEntity): The user entity containing updated user data.

        Returns:
            UpdateUserOutput: A DTO containing the mapped user update response.
        """
        return cls(
            user_id=entity.user_id,
            name=entity.name,
            email=entity.email,
            status=entity.status,
            role_id=entity.role_id,
        )

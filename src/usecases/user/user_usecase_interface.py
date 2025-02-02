# /src/usecases/user/user_usecase_interface.py

from abc import ABC, abstractmethod

from src.core.dtos.user.user_dto import UserRequestDTO, UserResponseDTO


class UserUseCaseInterface(ABC):
    """
    #TODO: define docstrings
    """

    @abstractmethod
    def create_user(self, request: UserRequestDTO) -> UserResponseDTO:
        pass

    @abstractmethod
    def get_users(self):
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> UserResponseDTO:
        pass

# /src/core/dtos/login_dto.py


from pydantic import BaseModel, RootModel


class LoginRequestDTO(BaseModel):
    """
    Class responsible for the Data Transfer Object (DTO) for user login requests.

    This class is used to validate and structure login request payloads.

    Class Args:
        None
    """

    email: str
    password: str


class LoginResponseDTO(RootModel):
    """
    Data Transfer Object (DTO) for user login responses.

    This class structures the login response, returning authentication-related data.

    Class Args:
        None
    """

    root: dict[str, str]

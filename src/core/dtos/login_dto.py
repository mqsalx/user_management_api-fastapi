# /src/core/dtos/login_dto.py


from pydantic import BaseModel, RootModel


class LoginRequestDTO(BaseModel):
    email: str
    password: str


class LoginResponseDTO(RootModel):
    root: dict[str, str]

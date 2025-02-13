# /src/core/dtos/login_dto.py

from pydantic import BaseModel, ConfigDict


class LoginRequestDTO(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(extra="forbid")


class LoginResponseDTO(BaseModel):

    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)


# class LoginResponseDTO(BaseModel):

#     name: str
#     email: str

#     model_config = ConfigDict(from_attributes=True)

# /src/core/dtos/login_dto.py


from pydantic import BaseModel, ConfigDict, RootModel


class LoginRequestDTO(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(extra="forbid")


class LoginResponseDTO(RootModel):
    root: dict[str, str]


# class LoginResponseDTO(BaseModel):

#     name: str
#     email: str

#     model_config = ConfigDict(from_attributes=True)

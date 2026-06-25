from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from constants.roles import Roles


class RegisterUserRequest(BaseModel):

    model_config = ConfigDict(use_enum_values=True)

    email: EmailStr
    fullName: str = Field(min_length=1, max_length=100)

    password: str = Field(min_length=8)
    passwordRepeat: str = Field(min_length=8)

    roles: List[Roles] = Field(default_factory=lambda: [Roles.USER])

    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @field_validator("passwordRepeat")
    @classmethod
    def passwords_match(cls, value, info):
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Passwords do not match")
        return value


class RegisterUserResponse(BaseModel):

    model_config = ConfigDict(use_enum_values=True)

    id: str
    email: EmailStr
    fullName: str
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: datetime

class MovieResponse(BaseModel):
        id: int
        name: str
        description: str
        price: int
        location: str
        published: bool
        genreId: int
        reviews: list = []

class ApiErrorResponse(BaseModel):
        statusCode: int
        message: str

class MoviesListResponse(BaseModel):
        movies: list[MovieResponse]
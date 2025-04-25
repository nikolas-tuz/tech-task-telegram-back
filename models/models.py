from bson import ObjectId
from pydantic import BaseModel, EmailStr, validator


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class User(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 5:
            raise ValueError("Password must be at least 5 characters long")
        return value

    class Config:
        json_encoders = {ObjectId: str}

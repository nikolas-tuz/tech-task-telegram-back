from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True

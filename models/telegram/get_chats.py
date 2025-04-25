from typing import Optional

from pydantic import BaseModel


class GetChatsRequest(BaseModel):
    phone_number: str
    code: int
    phone_code_hash: str
    password: Optional[str]

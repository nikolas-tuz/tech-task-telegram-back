from pydantic import BaseModel


class SendCodeToPhoneRequest(BaseModel):
    phone_number: str

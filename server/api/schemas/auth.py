from pydantic import BaseModel


class Login(BaseModel):
    # Schema for the input required by the input endpoint
    email: str
    password: str

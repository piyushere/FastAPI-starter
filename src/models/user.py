from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: EmailStr

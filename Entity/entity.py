from pydantic import BaseModel, BaseSettings, ValidationError, validator, Field
from typing import Optional, List
from enum import Enum
import os

class Adminentity(BaseModel):
    storename : str
    account : str
    password : str

    class Config: orm_mode = True
    # @validator('password')
    # def password_rules(cls, v, values, **kwargs):
    #     if len(v) < 8:
    #         raise ValueError('password too short')
    #     if v.isalnum() or len(set(v)) <= 3:
    #         raise ValueError('password too simple')
    #     return v

    # @validator('username')
    # def username_alphanumeric(cls, v):
    #     assert v.isalnum(), 'must be alphanumeric'
    #     return v

#example
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

#example
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
# print(Color.GREEN.name)
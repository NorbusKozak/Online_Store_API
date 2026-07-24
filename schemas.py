from pydantic import BaseModel, EmailStr, ConfigDict, PositiveInt, PositiveFloat
from typing import List


class UserCreateValidator(BaseModel):
    email: EmailStr
    password: str 

class UserResponseValidator(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_admin: bool

class ProductValidator(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str
    price: PositiveFloat
    stock: PositiveInt

class ProductResponseValidator(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: PositiveFloat
    stock: PositiveInt


class ItemAddToCartValidator(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt

class OrderCreateValidator(BaseModel):
    items: List[ItemAddToCartValidator]

class OrderResponseValidator(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    total_price: float

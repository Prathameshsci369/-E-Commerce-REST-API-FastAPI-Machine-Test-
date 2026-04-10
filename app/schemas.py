from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import relationship

class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    price: float
    category_id: int

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

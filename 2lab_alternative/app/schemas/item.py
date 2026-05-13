from pydantic import BaseModel, Field
from typing import List, Optional
from .price import PriceResponse

class ItemBase(BaseModel):
    title: str = Field(..., min_length=2)
    description: Optional[str] = None

class ItemCreate(ItemBase):
    source_id: int

class ItemUpdate(ItemBase):
    source_id: int

class ItemPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    source_id: Optional[int] = None

class ItemResponse(ItemBase):
    id: int
    source_id: int
    prices: List[PriceResponse] = [] # Вложенная схема

    class Config:
        from_attributes = True
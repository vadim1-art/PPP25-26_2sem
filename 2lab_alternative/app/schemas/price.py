from pydantic import BaseModel, Field
from datetime import datetime

class PriceBase(BaseModel):
    amount: float = Field(..., gt=0)

class PriceCreate(PriceBase):
    pass

class PriceResponse(PriceBase):
    id: int
    recorded_at: datetime
    item_id: int

    class Config:
        from_attributes = True
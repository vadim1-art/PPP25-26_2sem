from pydantic import BaseModel, Field

class SourceBase(BaseModel):
    name: str = Field(..., min_length=2)
    url: str

class SourceCreate(SourceBase):
    pass

class SourceResponse(SourceBase):
    id: int
    class Config:
        from_attributes = True
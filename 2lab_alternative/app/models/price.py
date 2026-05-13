from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    item = relationship("Item", back_populates="prices")
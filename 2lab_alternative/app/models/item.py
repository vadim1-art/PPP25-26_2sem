from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)

    # Связи через строковые литералы
    source = relationship("Source", back_populates="items")
    prices = relationship("Price", back_populates="item", cascade="all, delete-orphan")
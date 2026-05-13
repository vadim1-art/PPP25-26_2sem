from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    # Используем строковое имя класса "Item" для связи
    items = relationship("Item", back_populates="source", cascade="all, delete-orphan")
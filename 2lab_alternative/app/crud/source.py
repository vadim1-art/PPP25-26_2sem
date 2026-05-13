from sqlalchemy.orm import Session
from app.models.source import Source
from app.schemas.source import SourceCreate

def get_sources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Source).offset(skip).limit(limit).all()

def create_source(db: Session, source_in: SourceCreate):
    db_source = Source(**source_in.model_dump())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source
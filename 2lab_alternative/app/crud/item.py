from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemPatch

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def create_item(db: Session, item_in: ItemCreate):
    db_item = Item(**item_in.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, db_item: Item, item_in: ItemUpdate):
    for key, val in item_in.model_dump().items():
        setattr(db_item, key, val)
    db.commit()
    db.refresh(db_item)
    return db_item

def patch_item(db: Session, db_item: Item, item_in: ItemPatch):
    data = item_in.model_dump(exclude_unset=True)
    for key, val in data.items():
        setattr(db_item, key, val)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, db_item: Item):
    db.delete(db_item)
    db.commit()
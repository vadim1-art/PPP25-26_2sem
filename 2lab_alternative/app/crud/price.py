from sqlalchemy.orm import Session
from app.models.price import Price
from app.schemas.price import PriceCreate

def get_prices_by_item(db: Session, item_id: int):
    return db.query(Price).filter(Price.item_id == item_id).all()

def create_price(db: Session, price_in: PriceCreate, item_id: int):
    db_price = Price(**price_in.model_dump(), item_id=item_id)
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price
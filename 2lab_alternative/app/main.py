from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, get_db
from app.models import Base
from app import crud, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ETL Unified API")

# --- SOURCES ---
@app.get("/sources/", response_model=List[schemas.SourceResponse], tags=["Sources"])
def list_sources(db: Session = Depends(get_db)):
    return crud.get_sources(db)

@app.post("/sources/", response_model=schemas.SourceResponse, tags=["Sources"])
def add_source(source: schemas.SourceCreate, db: Session = Depends(get_db)):
    return crud.create_source(db, source)

# --- ITEMS ---
@app.get("/items/", response_model=List[schemas.ItemResponse], tags=["Items"])
def list_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get("/items/{item_id}", response_model=schemas.ItemResponse, tags=["Items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/", response_model=schemas.ItemResponse, tags=["Items"])
def add_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@app.put("/items/{item_id}", response_model=schemas.ItemResponse, tags=["Items"])
def full_update_item(item_id: int, item_in: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return crud.update_item(db, item, item_in)

@app.patch("/items/{item_id}", response_model=schemas.ItemResponse, tags=["Items"])
def partial_update_item(item_id: int, item_in: schemas.ItemPatch, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return crud.patch_item(db, item, item_in)

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
def remove_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, item)
    return None

# --- PRICES (Связанные данные) ---
@app.get("/items/{item_id}/prices/", response_model=List[schemas.PriceResponse], tags=["Prices"])
def read_item_prices(item_id: int, db: Session = Depends(get_db)):
    if not crud.get_item(db, item_id): raise HTTPException(status_code=404, detail="Item not found")
    return crud.get_prices_by_item(db, item_id)

@app.post("/items/{item_id}/prices/", response_model=schemas.PriceResponse, tags=["Prices"])
def add_price(item_id: int, price_in: schemas.PriceCreate, db: Session = Depends(get_db)):
    if not crud.get_item(db, item_id): raise HTTPException(status_code=404, detail="Item not found")
    return crud.create_price(db, price_in, item_id)
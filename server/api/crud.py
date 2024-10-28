# from fastapi import FastAPI, Depends, HTTPException,APIRouter
# from sqlalchemy.orm import Session
# from sqlmodel import SQLModel, Field, create_engine, Session

# router = APIRouter()

# class Item(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     name: str
#     description: str

# sqlite_url = "sqlite:///./test.db"
# engine = create_engine(sqlite_url, echo=True)

# @router.post("/items/", response_model=Item)
# async def create_item(item: Item, session: Session = Depends()):
#     session.add(item)
#     session.commit()
#     return item

# @router.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: int, session: Session = Depends()):
#     item = session.get(Item, item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item

from fastapi import FastAPI, status, Depends, HTTPException
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from auth import router
from auth import get_current_user

app = FastAPI()
app.include_router(router)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSessionDep = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: DbSessionDep):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {"User": user}
from fastapi import FastAPI , HTTPException, Depends
from pydantic import BaseModel , Field
from uuid import UUID
import models
from db  import engine , sessionLocal
from sqlalchemy.orm import Session

from typing import Optional


USERS = []

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = sessionLocal()
        yield db

    finally:
        db.close()


class User(BaseModel):
    name: Optional[str ]= Field(max_length=30)
    email: Optional[str] = Field(min_length=1)
    age: Optional[int] = Field(gt=0)



@app.get('/')
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@app.get('/{user_id}')
def get_user(user_id: int,db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    return user_model

 

@app.post('/')
def create_book(new_user: User , db: Session = Depends(get_db)):
    user_model = models.Users()
    user_model.name = new_user.name
    user_model.email = new_user.email
    user_model.age = new_user.age

    db.add(user_model)
    db.commit()



    return new_user

@app.put('/{user_id}')
def update_user(user_id: int, updated_user: User , db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()


    if user_model is None:
        raise HTTPException(status_code=404,
        detail=f"ID{user_id} not found")    
    if updated_user.name != None:
        user_model.name = updated_user.name
    if updated_user.email != None:
        user_model.email = updated_user.email
    if updated_user.age != None:
        user_model.age = updated_user.age
    
    db.add(user_model)
    db.commit()

    return updated_user

@app.delete('/{user_id}')
def delete_user(user_id: int , db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()

    
    if user_model is None:
        raise HTTPException(status_code=404,
        detail=f"ID{user_id} not found")    

    db.query(models.Users).filter(models.Users.id == user_id).delete()
    db.commit()

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class User(BaseModel):
    name: str = Field(min_length=1)#lo rojo es la longitud
    id: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=5000)
    age: int = Field(gt=-1, lt=101)#mayor a menos uno y menor que 101
    recommendations: str = Field(min_length=1)
    zip: int = Field(gt=-1, lt=101)

@app.post("/")
def create_book(user: User, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.name = user.name
   # user_model.id = book.author
    user_model.email = user.email
    user_model.age = user.age
    user_model.recommendations =user.recommendations
    user_model.zip = user.zip
#agregalo y sube los cambios
    db.add(user_model)
    db.commit()

    return user


if __name__ == "__main__":
    if __name__ == "__main__":
        uvicorn.run("user:app", host="0.0.0.0", port=5050, log_level="info", reload=True)


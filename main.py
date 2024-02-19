### `books.py`
#PRINCIPAL
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()
#crea una tabla con el esquema definido si es que no existe todavia y hace la conexión
models.Base.metadata.create_all(bind=engine)

#permite hacer las operaciones CRUD
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#se comunica entre la API y post man como body parameter.
class User(BaseModel):
    user_name: str = Field(min_length=1)#lo rojo es la longitud
    user_id: str = Field(min_length=1, max_length=100)
    user_email: str = Field(min_length=1, max_length=5000)
    age: int = Field(gt=-1, lt=101)#mayor a menos uno y menor que 101
    recommendations: str = Field(min_length=1)
    zip: int = Field(gt=-1, lt=101)

#db viene de get_db
@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Books).all()
#te va a regresar el esquema del la bd, lo cual al principio es vacío porque no se ha creado

#es la misma estructura para todos los CRUD
@app.post("/")
def create_book(book: Book, db: Session = Depends(get_db)):
#lo que agregue en postman se guarda en la variable book de la clase Book
    book_model = models.Books()#ESQUEMA de los libros
    book_model.title = book.title#del body request asignaleel titulo
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating
#agregalo y sube los cambios
    db.add(book_model)
    db.commit()

    return book

#operación put es para ACTUALIZAR
@app.put("/{book_id}")
def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
#where la columna de id coincida con la que yo le estoy dando
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
        )
#si no se aplica la excepción se agregan los cambios
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book


@app.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):

    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {book_id} : Does not exist"
        )

    db.query(models.Books).filter(models.Books.id == book_id).delete()

    db.commit()

if __name__ == "__main__":
    uvicorn.run("books:app
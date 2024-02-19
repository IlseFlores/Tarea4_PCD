from sqlalchemy import Column, Integer, String
from database import Base

#esquema de mi base de datos
#define el esquema de mi tabla
class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    description = Column(String)
    rating = Column(Integer)

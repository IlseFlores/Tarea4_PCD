from sqlalchemy import Column, Integer, String
from database import Base

#esquema de mi base de datos
#define el esquema de mi tabla
class Users(Base):
    __tablename__ = "main"

    name = Column(String)
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    age = Column(Integer)
    recommendations = Column(String)
    zip = Column(String)


from sqlalchemy.ext.declarative import declarative_base
#url de mi db
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"
#motor de conexión para mi db
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#conexión local entre python y nuestra base de datod
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#permite hacer el CRUD en nuestra base de datos
Base = declarative_base()
from database import engine
from models import Base

def create_db():
    # Создание таблиц в базе данных
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_db()

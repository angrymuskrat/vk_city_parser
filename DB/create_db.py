from database import engine
from models import Base


def create_db():
    with engine.connect() as connection:
        connection.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_db()

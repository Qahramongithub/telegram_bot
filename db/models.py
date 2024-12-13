import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, Session
from sqlalchemy.orm import Mapped, mapped_column

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


engine = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:10075/{DB_NAME}'
)
session = Session(bind=engine)


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    staff: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)


    def __repr__(self):
        return f'User(id{self.id}, staff{self.staff})'

class Branche(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True)
    latitude : Mapped[float] = mapped_column(nullable=True)
    longitude : Mapped[float] = mapped_column(nullable=True)
    radius : Mapped[int] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)


class Att(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(nullable=True)
    staff: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)
    time: Mapped[str] = mapped_column(nullable=True)
    date_time: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[str] = mapped_column(nullable=True)


class Login(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True,nullable=True)
    admin_id:Mapped[str] =mapped_column(nullable=True)
    password:Mapped[str] = mapped_column(nullable=True)



Base.metadata.create_all(engine)

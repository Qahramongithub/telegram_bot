import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, declared_attr, Session
from sqlalchemy.orm import Mapped, mapped_column
import psycopg2
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


engine = create_engine(
    'postgresql+psycopg2://developer:Developer2024@postgresql-188855-0.cloudclusters.net:10075/production_db'
)
session = Session(bind=engine)


class Base(DeclarativeBase):
    pass
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    staff: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    price : Mapped[float] = mapped_column()

    def __repr__(self):
        return f'User(id{self.id}, staff{self.staff})'

class Branche(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    latitude : Mapped[float] = mapped_column()
    longitude : Mapped[float] = mapped_column()
    radius : Mapped[int] = mapped_column()

# class Employee(Base):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
#     date : Mapped[str] = mapped_column()
#     start_at: Mapped[str] = mapped_column()
#     latitude : Mapped[float] = mapped_column()
#     longitude : Mapped[float] = mapped_column()
#     status : Mapped[str] = mapped_column(unique=True)

class Att(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    staff: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    time: Mapped[str] = mapped_column()
    date_time: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column()

class Finance(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    date: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()

class Login(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    admin_id:Mapped[str] =mapped_column()
    password:Mapped[str] = mapped_column()



Base.metadata.create_all(engine)

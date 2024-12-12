import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, BigInteger
from sqlalchemy.orm import DeclarativeBase, declared_attr, Session
from sqlalchemy.orm import Mapped, mapped_column

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


engine = create_engine(
    'postgresql+psycopg2://developer:Developer2024@postgresql-188855-0.cloudclusters.net:10075/locations_db'
)
session = Session(bind=engine)


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    staff: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()


    def __repr__(self):
        return f'User(id{self.id}, staff{self.staff})'

class Branche(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True)
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
    date: Mapped[str] = mapped_column(nullable=True)
    staff: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)
    time: Mapped[str] = mapped_column(nullable=True)
    date_time: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[str] = mapped_column(nullable=True)

class Finance(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=True)
    date: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=True)

class Login(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True,nullable=True)
    admin_id:Mapped[str] =mapped_column(nullable=True)
    password:Mapped[str] = mapped_column(nullable=True)



Base.metadata.create_all(engine)

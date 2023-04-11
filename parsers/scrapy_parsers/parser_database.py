from pathlib import Path

from sqlalchemy import create_engine, Table, MetaData, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker
import uuid

from env import DB_USER, DB_PASSWORD

current_dir = Path(__file__).resolve().parent.parent.parent

base = current_dir / 'db.sqlite3'
DATABASE = {
    'drivername': 'sqlite',
    'database': str(base)
}

# engine = create_engine(URL(**DATABASE))
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost/sokrat")
Base = declarative_base(engine)


class Course(Base):
    __tablename__ = 'courses_course'
    __table_args__ = {'autoload': True}


class CoursePrice(Base):
    __tablename__ = 'courses_courseprice'
    __table_args__ = {'autoload': True}


class StudyPartner(Base):
    __tablename__ = 'study_partners_studypartner'
    __table_args__ = {'autoload': True}


class TypeOfLearning(Base):
    __tablename__ = 'courses_typeoflearning'
    __table_args__ = {'autoload': True}


class Status(Base):
    __tablename__ = 'courses_status'
    __table_args__ = {'autoload': True}


class CourseOrigin(Base):
    __tablename__ = 'courses_courseorigin'
    __table_args__ = {'autoload': True}


# def load_session():
#     metadata = Base.metadata
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session


def load_session():
    metadata = Base.metadata
    return sessionmaker(bind=engine)()

from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from parsers.env import DB_USER, DB_PASSWORD

# current_dir = Path(__file__).resolve().parent.parent.parent.parent
#
# base = current_dir / 'db.sqlite3'
# DATABASE = {
#     'drivername': 'sqlite',
#     'database': str(base)
# }
#
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


def load_session():
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///tackletask_tracker.db")
Session = sessionmaker(bind=engine)
session = Session()

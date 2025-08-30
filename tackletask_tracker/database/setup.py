import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_folder = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_folder, "tackletask_tracker.db")

Base = declarative_base()
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
session = Session()

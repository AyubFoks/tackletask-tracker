from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database.setup import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

    projects = relationship("Project", back_populates="client", cascade="all, delete-orphan")

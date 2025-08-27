from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database.setup import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hours_worked = Column(Float)
    rate_per_hour = Column(Float)
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(String, default="Pending")

    project = relationship("Project", back_populates="tasks")

    @property
    def earnings(self) -> float:
        """Calculates the earnings for a task."""
        return self.hours_worked * self.rate_per_hour

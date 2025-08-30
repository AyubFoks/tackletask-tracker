from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database.setup import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    deadline = Column(Date)
    client_id = Column(Integer, ForeignKey("clients.id"))
    project_status = Column(String, default="Pending")

    client = relationship("Client", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    @property
    def project_earnings(self) -> float:
        """Calculates the total earnings for a project."""
        return sum(task.earnings for task in self.tasks)

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from database.setup import Base

PROJECT_STATUS_CHOICES = ('Pending', 'In Progress', 'Completed')
TASK_STATUS_CHOICES = ('Pending', 'In Progress', 'Completed')


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    projects = relationship("Project", back_populates="client")


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    deadline = Column(Date)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship("Client", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    project_status = Column(
        Enum(*PROJECT_STATUS_CHOICES, name="project_status_enum"),
        default='Pending',
        nullable=False
    )

    @property
    def project_earnings(self):
        return sum(task.earnings for task in self.tasks)


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hours_worked = Column(Float)
    rate_per_hour = Column(Float)
    status = Column(
        Enum(*TASK_STATUS_CHOICES, name="task_status_enum"),
        default='Pending',
        nullable=False
    )
    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship("Project", back_populates="tasks")

    @property
    def earnings(self):
        return self.hours_worked * self.rate_per_hour

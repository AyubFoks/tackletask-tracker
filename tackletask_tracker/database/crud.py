from sqlalchemy.orm import Session
from . import models
from datetime import datetime
from typing import List


def get_client(db: Session, client_id: int) -> models.Client:
    """Gets a client by ID."""
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100) -> List[models.Client]:
    """Gets all clients."""
    return db.query(models.Client).offset(skip).limit(limit).all()


def create_client(db: Session, client: models.Client) -> models.Client:
    """Creates a new client."""
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def update_client(db: Session, client_id: int, client: models.Client) -> models.Client:
    """Updates a client."""
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    db_client.name = client.name
    db_client.email = client.email
    db_client.phone = client.phone
    db.commit()
    db.refresh(db_client)
    return db_client


def delete_client(db: Session, client_id: int) -> None:
    """Deletes a client."""
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    db.delete(db_client)
    db.commit()


def get_project(db: Session, project_id: int) -> models.Project:
    """Gets a project by ID."""
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[models.Project]:
    """Gets all projects."""
    return db.query(models.Project).offset(skip).limit(limit).all()


def get_projects_by_client(db: Session, client_id: int) -> List[models.Project]:
    """Gets all projects for a client."""
    return db.query(models.Project).filter(models.Project.client_id == client_id).all()


def get_projects_by_deadline(db: Session, deadline: datetime) -> List[models.Project]:
    """Gets all projects with a specific deadline."""
    return db.query(models.Project).filter(models.Project.deadline == deadline).all()


def create_project(db: Session, project: models.Project) -> models.Project:
    """Creates a new project."""
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project_id: int, project: models.Project) -> models.Project:
    """Updates a project."""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    db_project.title = project.title
    db_project.description = project.description
    db_project.deadline = project.deadline
    db_project.project_status = project.project_status
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> None:
    """Deletes a project."""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    db.delete(db_project)
    db.commit()


def get_task(db: Session, task_id: int) -> models.Task:
    """Gets a task by ID."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[models.Task]:
    """Gets all tasks."""
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_tasks_by_project(db: Session, project_id: int) -> List[models.Task]:
    """Gets all tasks for a project."""
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()


def get_tasks_by_deadline(db: Session, deadline: datetime) -> List[models.Task]:
    """Gets all tasks with a specific deadline."""
    return db.query(models.Task).join(models.Project).filter(models.Project.deadline == deadline).all()


def create_task(db: Session, task: models.Task) -> models.Task:
    """Creates a new task."""
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: int, task: models.Task) -> models.Task:
    """Updates a task."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db_task.name = task.name
    db_task.hours_worked = task.hours_worked
    db_task.rate_per_hour = task.rate_per_hour
    db_task.status = task.status
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> None:
    """Deletes a task."""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    db.delete(db_task)
    db.commit()

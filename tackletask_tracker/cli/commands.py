
import click
import re
from datetime import datetime
from typing import Dict, List

from rich.console import Console
from rich.table import Table

from ..database import crud
from ..database.setup import session
from ..models import Client, Project, Task
from .constants import (
    MAIN_MENU_OPTIONS,
    SUBMENU_OPTIONS,
    FILTER_PROJECTS_OPTIONS,
    FILTER_TASKS_OPTIONS,
)

EMAIL_REGEX = r"^\S+@\S+\.\S+$"


def show_menu(main_menu: bool = False) -> int:
    """Displays the main menu and returns the user's choice."""
    if main_menu:
        click.echo(
            "\n================================== \n👋 Hello, \nWelcome to TackleTask Tracker - your productivity partner. \n"
        )
    else:
        click.echo(
            "\n---------------------------------- \n \nHow else can I help you?")

    for key, value in MAIN_MENU_OPTIONS.items():
        click.echo(f"{key}. {value}")

    while True:
        try:
            choice = click.prompt("\nEnter your choice", type=int)
            if choice in MAIN_MENU_OPTIONS:
                return choice
            else:
                click.echo(
                    "\n⚠️\nEntry invalid! Please enter a valid option. \n")
        except click.Abort:
            raise
        except Exception:
            click.echo("\n⚠️\nEntry invalid! Please enter a valid option. \n")


def submenu(options: Dict[int, str]) -> int:
    """Displays a submenu with the given options and returns the user's choice."""
    while True:
        for key, value in options.items():
            click.echo(f"{key}. {value}")

        try:
            sub_choice = click.prompt("\nEnter your choice", type=int)
            if sub_choice in options:
                return sub_choice
            else:
                click.echo(
                    "\n⚠️\nEntry invalid! Please enter a valid option. \n")
        except click.Abort:
            raise
        except Exception:
            click.echo("\n⚠️\nEntry invalid! Please enter a valid option. \n")


def add_menu() -> None:
    """Displays the add menu and handles adding new objects to the database."""
    click.echo("\n____Add____")
    choice = submenu(SUBMENU_OPTIONS["add"])
    if choice == 0:
        return
    elif choice == 1:
        add_client()
    elif choice == 2:
        add_project()
    elif choice == 3:
        add_task()


def add_client() -> None:
    """Prompts the user for client information and adds the client to the database."""
    name = click.prompt("Client name")
    while True:
        email = click.prompt("Client email")
        if re.match(EMAIL_REGEX, email):
            break
        else:
            click.echo("Invalid email format. Please try again.")
    phone = click.prompt("Client phone")
    client = Client(name=name, email=email, phone=phone)
    created_client = crud.create_client(session, client)
    click.echo("\n✔️\nClient added successfully.")
    click.echo(
        f"ID: {created_client.id}, Name: {created_client.name}, Email: {created_client.email}, Phone: {created_client.phone}"
    )


def add_project() -> None:
    """Prompts the user for project information and adds the project to the database."""
    title = click.prompt("Project title")
    description = click.prompt("Project description")
    while True:
        deadline_str = click.prompt("Project deadline (YYYY-MM-DD)")
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            break
        except ValueError:
            click.echo("Invalid date format. Please use YYYY-MM-DD.")
    client_id = click.prompt("Client ID")
    project = Project(
        title=title,
        description=description,
        deadline=deadline,
        client_id=client_id,
    )
    created_project = crud.create_project(session, project)
    click.echo("\n✔️\nProject added successfully. \n")
    click.echo(
        f"ID: {created_project.id}, Title: {created_project.title}, Status: {created_project.project_status}, Deadline: {created_project.deadline}, Client ID: {created_project.client_id}"
    )


def add_task() -> None:
    """Prompts the user for task information and adds the task to the database."""
    name = click.prompt("Task name")
    hours_worked = click.prompt("Hours worked", type=float)
    rate_per_hour = click.prompt("Rate per hour", type=float)
    project_id = click.prompt("Project ID")
    task = Task(
        name=name,
        hours_worked=hours_worked,
        rate_per_hour=rate_per_hour,
        project_id=project_id,
    )
    created_task = crud.create_task(session, task)
    click.echo("\n✔️\nTask added successfully. \n")
    click.echo(
        f"ID: {created_task.id}, Name: {created_task.name}, Status: {created_task.status}, Project ID: {created_task.project_id}, Earnings: {created_task.earnings}"
    )


def view_menu() -> None:
    """Displays the view menu and handles viewing objects from the database."""
    click.echo("\n____View____")
    choice = submenu(SUBMENU_OPTIONS["view"])
    if choice == 0:
        return
    elif choice == 1:
        view_clients()
    elif choice == 2:
        view_projects()
    elif choice == 3:
        view_tasks()
    elif choice == 4:
        view_earnings()


def view_clients() -> None:
    """Displays all clients from the database."""
    clients = crud.get_clients(session)
    if not clients:
        click.echo("\n⚠️\nData not available! Add data first. \n")
        return

    table = Table(title="Clients")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Phone", style="yellow")

    for c in clients:
        table.add_row(str(c.id), c.name, c.email, c.phone)

    console = Console()
    console.print(table)


def view_projects() -> None:
    """Displays all projects from the database, with filtering options."""
    projects = crud.get_projects(session)
    if not projects:
        click.echo("\n⚠️\nData not available! Add data first. \n")
        return

    click.echo("\n____Filter Project by:____")
    filter_opt = submenu(FILTER_PROJECTS_OPTIONS)
    if filter_opt == 0:
        return
    if filter_opt == 1:
        client_id = click.prompt("Enter Client ID", type=int)
        projects = crud.get_projects_by_client(session, client_id)
    elif filter_opt == 2:
        while True:
            deadline_str = click.prompt("Enter deadline (YYYY-MM-DD)")
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                break
            except ValueError:
                click.echo("Invalid date format. Please use YYYY-MM-DD.")
        projects = crud.get_projects_by_deadline(session, deadline)
    elif filter_opt == 3:
        projects = crud.get_projects(session)

    if not projects:
        click.echo("\n⚠️\nData not available! Add data first. \n")
        return

    table = Table(title="Projects")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Deadline", style="yellow")
    table.add_column("Client ID", justify="right", style="cyan")

    for p in projects:
        table.add_row(
            str(p.id),
            p.title,
            p.project_status,
            str(p.deadline),
            str(p.client_id),
        )

    console = Console()
    console.print(table)


def view_tasks() -> None:
    """Displays all tasks from the database, with filtering options."""
    tasks = crud.get_tasks(session)
    if not tasks:
        click.echo("\n⚠️\nData not available! Add data first. \n")
        return

    click.echo("\n____Filter Tasks by:____")
    filter_opt = submenu(FILTER_TASKS_OPTIONS)
    if filter_opt == 0:
        return
    if filter_opt == 1:
        project_id = click.prompt("Enter Project ID", type=int)
        tasks = crud.get_tasks_by_project(session, project_id)
    elif filter_opt == 2:
        while True:
            deadline_str = click.prompt("Enter deadline (YYYY-MM-DD)")
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                break
            except ValueError:
                click.echo("Invalid date format. Please use YYYY-MM-DD.")
        tasks = crud.get_tasks_by_deadline(session, deadline)
    elif filter_opt == 3:
        tasks = crud.get_tasks(session)

    if not tasks:
        click.echo("\n⚠️\nData not available! Add data first. \n")
        return

    table = Table(title="Tasks")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Project ID", justify="right", style="cyan")
    table.add_column("Earnings", justify="right", style="green")

    for t in tasks:
        table.add_row(
            str(t.id), t.name, t.status, str(
                t.project_id), f"Ksh. {t.earnings}"
        )

    console = Console()
    console.print(table)


def view_earnings() -> None:
    """Displays total earnings or earnings for a specific project."""
    projects = crud.get_projects(session)
    if not projects:
        click.echo("\n⚠️\nData not available! Add data first. \n")
        return
    while True:
        try:
            project_id = click.prompt(
                "\nEnter Project ID for earnings or 0 for total earnings", type=int
            )
            if project_id == 0:
                total = sum(p.project_earnings for p in projects)
                click.echo(f"Total earnings: Ksh. {total}")
                break
            else:
                project = crud.get_project(session, project_id)
                if project:
                    click.echo(
                        f"Earnings for Project {project_id}: Ksh. {project.project_earnings}"
                    )
                    break
                else:
                    click.echo("\n⚠️\nData not available! Add data first. \n")
        except Exception:
            click.echo("\n⚠️\nEntry invalid! Please enter a valid option. \n")


def update_menu() -> None:
    """Displays the update menu and handles updating objects in the database."""
    click.echo("\n____Update____")
    choice = submenu(SUBMENU_OPTIONS["update"])
    if choice == 0:
        return
    elif choice == 1:
        update_client()
    elif choice == 2:
        update_project()
    elif choice == 3:
        update_task()


def update_client() -> None:
    """Prompts the user for client ID and new information, then updates the client in the database."""
    client_id = click.prompt("Enter Client ID to update", type=int)
    client = crud.get_client(session, client_id)
    if client:
        client.name = click.prompt("New name", default=client.name)
        while True:
            email = click.prompt("New email", default=client.email)
            if re.match(EMAIL_REGEX, email):
                break
            else:
                click.echo("Invalid email format. Please try again.")
        client.phone = click.prompt("New phone", default=client.phone)
        updated_client = crud.update_client(session, client_id, client)
        click.echo("\n✔️\nClient updated succesfully. \n")
        click.echo(
            f"ID: {updated_client.id}, Name: {updated_client.name}, Email: {updated_client.email}, Phone: {updated_client.phone}"
        )
    else:
        click.echo("\n⚠️\nData not available! Add data first. \n")


def update_project() -> None:
    """Prompts the user for project ID and new information, then updates the project in the database."""
    project_id = click.prompt("Enter Project ID to update", type=int)
    project = crud.get_project(session, project_id)
    if project:
        project.title = click.prompt("New title", default=project.title)
        project.description = click.prompt(
            "New description", default=project.description
        )
        while True:
            deadline_str = click.prompt(
                "New deadline (YYYY-MM-DD)",
                default=project.deadline.strftime("%Y-%m-%d"),
            )
            try:
                project.deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                break
            except ValueError:
                click.echo("Invalid date format. Please use YYYY-MM-DD.")
        project.project_status = click.prompt(
            "New status",
            type=click.Choice(["Pending", "In Progress", "Completed"]),
            default=project.project_status,
        )
        updated_project = crud.update_project(session, project_id, project)
        click.echo("\n✔️\nProject updated succesfully. \n")
        click.echo(
            f"ID: {updated_project.id}, Title: {updated_project.title}, Status: {updated_project.project_status}, Deadline: {updated_project.deadline}, Client ID: {updated_project.client_id}"
        )
    else:
        click.echo("\n⚠️\nData not available! Add data first. \n")


def update_task() -> None:
    """Prompts the user for task ID and new information, then updates the task in the database."""
    task_id = click.prompt("Enter Task ID to update", type=int)
    task = crud.get_task(session, task_id)
    if task:
        task.name = click.prompt("New name", default=task.name)
        task.hours_worked = click.prompt(
            "New hours worked", type=float, default=task.hours_worked
        )
        task.rate_per_hour = click.prompt(
            "New rate per hour", type=float, default=task.rate_per_hour
        )
        task.status = click.prompt(
            "New status",
            type=click.Choice(["Pending", "In Progress", "Completed"]),
            default=task.status,
        )
        updated_task = crud.update_task(session, task_id, task)
        click.echo("\n✔️\nTask updated succesfully. \n")
        click.echo(
            f"ID: {updated_task.id}, Name: {updated_task.name}, Status: {updated_task.status}, Project ID: {updated_task.project_id}, Earnings: {updated_task.earnings}"
        )
    else:
        click.echo("\n⚠️\nData not available! Add data first. \n")


def delete_menu() -> None:
    """Displays the delete menu and handles deleting objects from the database."""
    click.echo("\n____Delete____")
    choice = submenu(SUBMENU_OPTIONS["delete"])
    if choice == 0:
        return
    elif choice == 1:
        delete_client()
    elif choice == 2:
        delete_project()
    elif choice == 3:
        delete_task()


def delete_client() -> None:
    """Prompts the user for a client ID and deletes the client from the database."""
    client_id = click.prompt("Enter Client ID to delete", type=int)
    crud.delete_client(session, client_id)
    click.echo("\n Client and all associated projects deleted.")


def delete_project() -> None:
    """Prompts the user for a project ID and deletes the project from the database."""
    project_id = click.prompt("Enter Project ID to delete", type=int)
    crud.delete_project(session, project_id)
    click.echo("\nProject and all associated tasks deleted. \n")


def delete_task() -> None:
    """Prompts the user for a task ID and deletes the task from the database."""
    task_id = click.prompt("Enter Task ID to delete", type=int)
    crud.delete_task(session, task_id)
    click.echo("\nTask deleted. \n")


@click.command()
def cli() -> None:
    """Main CLI entry point."""
    choice = show_menu(main_menu=True)
    while choice != 0:
        if choice == 1:
            add_menu()
        elif choice == 2:
            view_menu()
        elif choice == 3:
            update_menu()
        elif choice == 4:
            delete_menu()
        choice = show_menu()

    click.echo(
        "\nThank you for using TackleTask Tracker. \nGoodbye!😉 \n=========================================== \n"
    )

import argparse
import re
from datetime import datetime
from typing import Dict, List

from rich.console import Console
from rich.table import Table
from rich import box

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
        print(
            "\n================================== \n👋 Hello, \nWelcome to TackleTask Tracker - your productivity partner. \n"
        )
    else:
        print(
            "\n---------------------------------- \n \nHow else can I help you?"
        )

    for key, value in MAIN_MENU_OPTIONS.items():
        print(f"{key}. {value}")

    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            if choice in MAIN_MENU_OPTIONS:
                return choice
            else:
                print(
                    "\n⚠️\nEntry invalid! Please enter a valid option. \n"
                )
        except ValueError:
            print("\n⚠️\nEntry invalid! Please enter a valid option. \n")

def submenu(options: Dict[int, str]) -> int:
    """Displays a submenu with the given options and returns the user's choice."""
    while True:
        for key, value in options.items():
            print(f"{key}. {value}")

        try:
            sub_choice = int(input("\nEnter your choice: "))
            if sub_choice in options:
                return sub_choice
            else:
                print(
                    "\n⚠️\nEntry invalid! Please enter a valid option. \n"
                )
        except ValueError:
            print("\n⚠️\nEntry invalid! Please enter a valid option. \n")

def add_menu() -> None:
    """Displays the add menu and handles adding new objects to the database."""
    print("\n____Add____")
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
    name = input("Client name: ")
    while True:
        email = input("Client email: ")
        if re.match(EMAIL_REGEX, email):
            break
        else:
            print("Invalid email format. Please try again.")
    phone = input("Client phone: ")
    client = Client(name=name, email=email, phone=phone)
    created_client = crud.create_client(session, client)
    print("\n✔️\nClient added successfully.")
    print(
        f"ID: {created_client.id}, Name: {created_client.name}, Email: {created_client.email}, Phone: {created_client.phone}"
    )

def add_project() -> None:
    """Prompts the user for project information and adds the project to the database."""
    title = input("Project title: ")
    description = input("Project description: ")
    while True:
        deadline_str = input("Project deadline (YYYY-MM-DD): ")
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    client_id = int(input("Client ID: "))
    project = Project(
        title=title,
        description=description,
        deadline=deadline,
        client_id=client_id,
    )
    created_project = crud.create_project(session, project)
    print("\n✔️\nProject added successfully. \n")
    print(
        f"ID: {created_project.id}, Title: {created_project.title}, Status: {created_project.project_status}, Deadline: {created_project.deadline}, Client ID: {created_project.client_id}"
    )

def add_task() -> None:
    """Prompts the user for task information and adds the task to the database."""
    name = input("Task name: ")
    hours_worked = float(input("Hours worked: "))
    rate_per_hour = float(input("Rate per hour: "))
    project_id = int(input("Project ID: "))
    task = Task(
        name=name,
        hours_worked=hours_worked,
        rate_per_hour=rate_per_hour,
        project_id=project_id,
    )
    created_task = crud.create_task(session, task)
    print("\n✔️\nTask added successfully. \n")
    print(
        f"ID: {created_task.id}, Name: {created_task.name}, Status: {created_task.status}, Project ID: {created_task.project_id}, Earnings: {created_task.earnings}"
    )

def view_menu() -> None:
    """Displays the view menu and handles viewing objects from the database."""
    print("\n____View____")
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
        print("\n⚠️\nData not available! Add data first. \n")
        return

    table = Table(
        title="Clients",
        box=box.ROUNDED,
        border_style="bright_blue",
        header_style="bold magenta",
        row_styles=["dim", ""],
    )
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Email", style="yellow")
    table.add_column("Phone", style="blue")

    for c in clients:
        table.add_row(str(c.id), c.name, c.email, c.phone)

    console = Console()
    console.print(table)


def view_projects() -> None:
    """Displays all projects from the database, with filtering options."""
    projects = crud.get_projects(session)
    if not projects:
        print("\n⚠️\nData not available! Add data first. \n")
        return

    print("\n____Filter Project by:____")
    filter_opt = submenu(FILTER_PROJECTS_OPTIONS)
    if filter_opt == 0:
        return
    if filter_opt == 1:
        client_id = int(input("Enter Client ID: "))
        projects = crud.get_projects_by_client(session, client_id)
    elif filter_opt == 2:
        while True:
            deadline_str = input("Enter deadline (YYYY-MM-DD): ")
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        projects = crud.get_projects_by_deadline(session, deadline)
    elif filter_opt == 3:
        projects = crud.get_projects(session)

    if not projects:
        print("\n⚠️\nData not available! Add data first. \n")
        return

    table = Table(
        title="Projects",
        box=box.ROUNDED,
        border_style="bright_green",
        header_style="bold cyan",
        row_styles=["dim", ""],
    )
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
        print("\n⚠️\nData not available! Add data first. \n")
        return

    print("\n____Filter Tasks by:____")
    filter_opt = submenu(FILTER_TASKS_OPTIONS)
    if filter_opt == 0:
        return
    if filter_opt == 1:
        project_id = int(input("Enter Project ID: "))
        tasks = crud.get_tasks_by_project(session, project_id)
    elif filter_opt == 2:
        while True:
            deadline_str = input("Enter deadline (YYYY-MM-DD): ")
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        tasks = crud.get_tasks_by_deadline(session, deadline)
    elif filter_opt == 3:
        tasks = crud.get_tasks(session)

    if not tasks:
        print("\n⚠️\nData not available! Add data first. \n")
        return

    table = Table(
        title="Tasks",
        box=box.ROUNDED,
        border_style="bright_yellow",
        header_style="bold blue",
        row_styles=["dim", ""],
    )
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Project ID", justify="right", style="cyan")
    table.add_column("Earnings", justify="right", style="green")

    for t in tasks:
        table.add_row(
            str(t.id), t.name, t.status, str(t.project_id), f"Ksh. {t.earnings}"
        )

    console = Console()
    console.print(table)


def view_earnings() -> None:
    """Displays total earnings or earnings for a specific project."""
    projects = crud.get_projects(session)
    if not projects:
        print("\n⚠️\nData not available! Add data first. \n")
        return
    while True:
        try:
            project_id = int(input(
                "\nEnter Project ID for earnings or 0 for total earnings: "
            ))
            if project_id == 0:
                total = sum(p.project_earnings for p in projects)
                print(f"Total earnings: Ksh. {total}")
                break
            else:
                project = crud.get_project(session, project_id)
                if project:
                    print(
                        f"Earnings for Project {project_id}: Ksh. {project.project_earnings}"
                    )
                    break
                else:
                    print("\n⚠️\nData not available! Add data first. \n")
        except ValueError:
            print("\n⚠️\nEntry invalid! Please enter a valid option. \n")

def update_menu() -> None:
    """Displays the update menu and handles updating objects in the database."""
    print("\n____Update____")
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
    client_id = int(input("Enter Client ID to update: "))
    client = crud.get_client(session, client_id)
    if client:
        name = input(f"New name [{client.name}]: ") or client.name
        while True:
            email = input(f"New email [{client.email}]: ") or client.email
            if re.match(EMAIL_REGEX, email):
                break
            else:
                print("Invalid email format. Please try again.")
        phone = input(f"New phone [{client.phone}]: ") or client.phone
        
        updated_client = crud.update_client(session, client_id, Client(name=name, email=email, phone=phone))
        print("\n✔️\nClient updated succesfully. \n")
        print(
            f"ID: {updated_client.id}, Name: {updated_client.name}, Email: {updated_client.email}, Phone: {updated_client.phone}"
        )
    else:
        print("\n⚠️\nData not available! Add data first. \n")

def update_project() -> None:
    """Prompts the user for project ID and new information, then updates the project in the database."""
    project_id = int(input("Enter Project ID to update: "))
    project = crud.get_project(session, project_id)
    if project:
        title = input(f"New title [{project.title}]: ") or project.title
        description = input(f"New description [{project.description}]: ") or project.description
        while True:
            deadline_str = input(f"New deadline (YYYY-MM-DD) [{project.deadline.strftime('%Y-%m-%d')}]: ") or project.deadline.strftime('%Y-%m-%d')
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        project_status = input(f"New status [{project.project_status}]: ") or project.project_status
        
        updated_project = crud.update_project(session, project_id, Project(title=title, description=description, deadline=deadline, project_status=project_status))
        print("\n✔️\nProject updated succesfully. \n")
        print(
            f"ID: {updated_project.id}, Title: {updated_project.title}, Status: {updated_project.project_status}, Deadline: {updated_project.deadline}, Client ID: {updated_project.client_id}"
        )
    else:
        print("\n⚠️\nData not available! Add data first. \n")

def update_task() -> None:
    """Prompts the user for task ID and new information, then updates the task in the database."""
    task_id = int(input("Enter Task ID to update: "))
    task = crud.get_task(session, task_id)
    if task:
        name = input(f"New name [{task.name}]: ") or task.name
        hours_worked = float(input(f"New hours worked [{task.hours_worked}]: ") or task.hours_worked)
        rate_per_hour = float(input(f"New rate per hour [{task.rate_per_hour}]: ") or task.rate_per_hour)
        status = input(f"New status [{task.status}]: ") or task.status
        
        updated_task = crud.update_task(session, task_id, Task(name=name, hours_worked=hours_worked, rate_per_hour=rate_per_hour, status=status))
        print("\n✔️\nTask updated succesfully. \n")
        print(
            f"ID: {updated_task.id}, Name: {updated_task.name}, Status: {updated_task.status}, Project ID: {updated_task.project_id}, Earnings: {updated_task.earnings}"
        )
    else:
        print("\n⚠️\nData not available! Add data first. \n")

def delete_menu() -> None:
    """Displays the delete menu and handles deleting objects from the database."""
    print("\n____Delete____")
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
    client_id = int(input("Enter Client ID to delete: "))
    client = crud.get_client(session, client_id)
    if client:
        crud.delete_client(session, client_id)
        print("\n Client and all associated projects deleted.")
    else:
        print("\n⚠️\nClient not found. \n")

def delete_project() -> None:
    """Prompts the user for a project ID and deletes the project from the database."""
    project_id = int(input("Enter Project ID to delete: "))
    project = crud.get_project(session, project_id)
    if project:
        crud.delete_project(session, project_id)
        print("\nProject and all associated tasks deleted. \n")
    else:
        print("\n⚠️\nProject not found. \n")

def delete_task() -> None:
    """Prompts the user for a task ID and deletes the task from the database."""
    task_id = int(input("Enter Task ID to delete: "))
    task = crud.get_task(session, task_id)
    if task:
        crud.delete_task(session, task_id)
        print("\nTask deleted. \n")
    else:
        print("\n⚠️\nTask not found. \n")

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

    print(
        "\nThank you for using TackleTask Tracker. \nGoodbye!😉 \n=========================================== \n"
    )

def main():
    parser = argparse.ArgumentParser(description="TackleTask Tracker - your productivity partner.")
    parser.add_argument('command', nargs='?', default=None, help="The command to execute.")

    args = parser.parse_args()

    if args.command:
        # This is a placeholder for future command-line specific functionality
        cli()
    else:
        cli()

if __name__ == "__main__":
    main()

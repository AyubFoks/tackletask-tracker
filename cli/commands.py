import click
from database.setup import session, Base, engine
from models import Client, Project, Task
from datetime import datetime


def main_menu():
    while True:
        click.echo(
            "\n================================== \nHello, \nWelcome to TackleTask Tracker - your productivity partner. \n\nHow can I assist you today? \n")
        click.echo("1. Add (client, project, task...)")
        click.echo("2. View (clients, projects, tasks, earnings...)")
        click.echo("3. Update (clients, projects, tasks...)")
        click.echo("4. Delete (clients, projects, tasks...)")
        click.echo("0. Exit")
        try:
            choice = click.prompt("\nEnter your choice", type=int)
            if choice in [0, 1, 2, 3, 4]:
                return choice
            else:
                click.echo("\nEntry Invalid! Enter a valid option. \n")
        except click.Abort:
            raise
        except Exception:
            click.echo("\nEntry Invalid! Enter a valid option. \n")


def submenu(options):
    while True:
        for idx, opt in enumerate(options, 1):
            click.echo(f"{idx}. {opt}")
        click.echo("0. Go back")
        try:
            sub_choice = click.prompt("\nEnter your choice", type=int)
            if 0 <= sub_choice <= len(options):
                return sub_choice
            else:
                click.echo("\nEntry Invalid! Enter a valid option. \n")
        except click.Abort:
            raise
        except Exception:
            click.echo("\nEntry Invalid! Enter a valid option. \n")


def add_menu():
    options = ["Client", "Project", "Task"]
    while True:
        choice = submenu(options)
        if choice == 0:
            return
        elif choice == 1:
            name = click.prompt("Client name")
            email = click.prompt("Client email")
            phone = click.prompt("Client phone")
            client = Client(name=name, email=email, phone=phone)
            session.add(client)
            session.commit()
            click.echo("Client added successfully.")
            return
        elif choice == 2:
            title = click.prompt("Project title")
            description = click.prompt("Project description")
            deadline = click.prompt("Project deadline (YYYY-MM-DD)")
            client_id = click.prompt("Client ID")
            project = Project(
                title=title,
                description=description,
                deadline=datetime.strptime(deadline, "%Y-%m-%d"),
                client_id=client_id
            )
            session.add(project)
            session.commit()
            click.echo("Project added successfully.")
            return
        elif choice == 3:
            name = click.prompt("Task name")
            hours_worked = click.prompt("Hours worked", type=float)
            rate_per_hour = click.prompt("Rate per hour", type=float)
            project_id = click.prompt("Project ID")
            task = Task(
                name=name,
                hours_worked=hours_worked,
                rate_per_hour=rate_per_hour,
                project_id=project_id
            )
            session.add(task)
            session.commit()
            click.echo("Task added successfully.")
            return


def view_menu():
    options = ["Clients", "Projects", "Tasks", "Earnings"]
    while True:
        choice = submenu(options)
        if choice == 0:
            return
        elif choice == 1:
            clients = session.query(Client).all()
            if not clients:
                click.echo("Data not available! Add data first.")
                return
            for c in clients:
                click.echo(
                    f"ID: {c.id}, Name: {c.name}, Email: {c.email}, Phone: {c.phone}")
            return
        elif choice == 2:
            projects = session.query(Project).all()
            if not projects:
                click.echo("Data not available! Add data first.")
                return
            while True:
                filter_opt = click.prompt(
                    "Filter by: 1. Client 2. Deadline 3. None 0. Go back", type=int)
                if filter_opt == 0:
                    break
                query = session.query(Project)
                if filter_opt == 1:
                    client_id = click.prompt("Enter Client ID", type=int)
                    query = query.filter(Project.client_id == client_id)
                elif filter_opt == 2:
                    deadline = click.prompt("Enter deadline (YYYY-MM-DD)")
                    query = query.filter(Project.deadline ==
                                         datetime.strptime(deadline, "%Y-%m-%d"))
                elif filter_opt == 3:
                    pass
                else:
                    click.echo("\nEntry Invalid! Enter a valid option. \n")
                    continue
                filtered_projects = query.all()
                if not filtered_projects:
                    click.echo("Data not available! Add data first.")
                    return
                for p in filtered_projects:
                    click.echo(
                        f"ID: {p.id}, Title: {p.title}, Status: {p.project_status}, Deadline: {p.deadline}, Client ID: {p.client_id}")
                break
            return
        elif choice == 3:
            tasks = session.query(Task).all()
            if not tasks:
                click.echo("Data not available! Add data first.")
                return
            while True:
                filter_opt = click.prompt(
                    "Filter by: 1. Project 2. Deadline 3. None 0. Go back", type=int)
                if filter_opt == 0:
                    break
                query = session.query(Task)
                if filter_opt == 1:
                    project_id = click.prompt("Enter Project ID", type=int)
                    query = query.filter(Task.project_id == project_id)
                elif filter_opt == 2:
                    deadline = click.prompt("Enter deadline (YYYY-MM-DD)")
                    query = query.join(Project).filter(
                        Project.deadline == datetime.strptime(deadline, "%Y-%m-%d"))
                elif filter_opt == 3:
                    pass
                else:
                    click.echo("\nEntry Invalid! Enter a valid option. \n")
                    continue
                filtered_tasks = query.all()
                if not filtered_tasks:
                    click.echo("Data not available! Add data first.")
                    return
                for t in filtered_tasks:
                    click.echo(
                        f"ID: {t.id}, Name: {t.name}, Status: {t.status}, Project ID: {t.project_id}, Earnings: {t.earnings}")
                break
            return
        elif choice == 4:
            projects = session.query(Project).all()
            if not projects:
                click.echo("Data not available! Add data first.")
                return
            while True:
                try:
                    project_id = click.prompt(
                        "Enter Project ID for earnings or 0 for total", type=int)
                    if project_id == 0:
                        total = sum(p.project_earnings for p in projects)
                        click.echo(f"Total earnings: {total}")
                        break
                    else:
                        project = session.query(Project).get(project_id)
                        if project:
                            click.echo(
                                f"Earnings for Project {project_id}: {project.project_earnings}")
                            break
                        else:
                            click.echo(
                                "\nEntry Invalid! Enter a valid option. \n")
                except Exception:
                    click.echo("\nEntry Invalid! Enter a valid option. \n")
            return


def update_menu():
    options = ["Client", "Project", "Task"]
    while True:
        choice = submenu(options)
        if choice == 0:
            return
        elif choice == 1:
            client_id = click.prompt("Enter Client ID to update", type=int)
            client = session.query(Client).get(client_id)
            if client:
                client.name = click.prompt("New name", default=client.name)
                client.email = click.prompt("New email", default=client.email)
                client.phone = click.prompt("New phone", default=client.phone)
                session.commit()
                click.echo("Client updated.")
                return
            else:
                click.echo("\nEntry Invalid! Enter a valid option. \n")
        elif choice == 2:
            project_id = click.prompt("Enter Project ID to update", type=int)
            project = session.query(Project).get(project_id)
            if project:
                project.title = click.prompt(
                    "New title", default=project.title)
                project.description = click.prompt(
                    "New description", default=project.description)
                project.deadline = datetime.strptime(
                    click.prompt("New deadline (YYYY-MM-DD)",
                                 default=project.deadline.strftime("%Y-%m-%d")),
                    "%Y-%m-%d"
                )
                project.project_status = click.prompt("New status", type=click.Choice(
                    ['Pending', 'In Progress', 'Completed']), default=project.project_status)
                session.commit()
                click.echo("Project updated.")
                return
            else:
                click.echo("\nEntry Invalid! Enter a valid option. \n")
        elif choice == 3:
            task_id = click.prompt("Enter Task ID to update", type=int)
            task = session.query(Task).get(task_id)
            if task:
                task.name = click.prompt("New name", default=task.name)
                task.hours_worked = click.prompt(
                    "New hours worked", type=float, default=task.hours_worked)
                task.rate_per_hour = click.prompt(
                    "New rate per hour", type=float, default=task.rate_per_hour)
                task.status = click.prompt("New status", type=click.Choice(
                    ['Pending', 'In Progress', 'Completed']), default=task.status)
                session.commit()
                click.echo("Task updated.")
                return
            else:
                click.echo("\nEntry Invalid! Enter a valid option. \n")


def delete_menu():
    options = ["Client", "Project", "Task"]
    while True:
        choice = submenu(options)
        if choice == 0:
            return
        elif choice == 1:
            client_id = click.prompt("Enter Client ID to delete", type=int)
            client = session.query(Client).get(client_id)
            if client:
                session.delete(client)
                session.commit()
                click.echo(
                    "Client and all associated projects and tasks deleted.")
                return
            else:
                click.echo("\nEntry Invalid! Enter a valid option. \n")
        elif choice == 2:
            project_id = click.prompt("Enter Project ID to delete", type=int)
            project = session.query(Project).get(project_id)
            if project:
                session.delete(project)
                session.commit()
                click.echo("Project and all associated tasks deleted.")
                return
            else:
                click.echo("\nEntry Invalid! Enter a valid option. \n")
        elif choice == 3:
            task_id = click.prompt("Enter Task ID to delete", type=int)
            task = session.query(Task).get(task_id)
            if task:
                session.delete(task)
                session.commit()
                click.echo("Task deleted.")
                return
            else:
                click.echo("\nEntry Invalid! Enter a valid option. \n")


@click.command()
def cli():
    while True:
        choice = main_menu()
        if choice == 0:
            break
        elif choice == 1:
            add_menu()
        elif choice == 2:
            view_menu()
        elif choice == 3:
            update_menu()
        elif choice == 4:
            delete_menu()
    click.echo(
        "\nThank you for using TackleTask Tracker. \nGoodbye!😉 \n===========================================\n")

# TackleTask Tracker

TackleTask Tracker is a simple command-line application for tracking clients, projects, and tasks. It provides a user-friendly interface to manage your freelance work efficiently.

## Features

*   Add, view, update, and delete clients, projects, and tasks.
*   View data in a clean and organized table format.
*   Filter projects by client and deadline.
*   Filter tasks by project and deadline.
*   View total earnings or earnings for a specific project.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Ayubfoks/tackletask-tracker.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd tackletask-tracker
    ```
3.  Create a virtual environment:
    ```bash
    python3 -m venv myenv
    ```
4.  Activate the virtual environment:
    ```bash
    source myenv/bin/activate
    ```
5.  Install the dependencies:
    ```bash
    pip install -r tackletask_tracker/requirements.txt
    ```

## Usage

To run the application, use the following command from the project's root directory:

```bash
python3 -m tackletask_tracker
```

This will launch the command-line interface, where you can add, view, update, and delete clients, projects, and tasks.

## Dependencies

*   [SQLAlchemy](https://www.sqlalchemy.org/): For database interactions.
*   [Click](https://click.palletsprojects.com/): For creating the command-line interface.
*   [Rich](https://rich.readthedocs.io/): For beautiful and informative table formatting.
*   [Pytest](https://docs.pytest.org/): For running tests.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
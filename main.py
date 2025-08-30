from tackletask_tracker.cli.commands import main
from tackletask_tracker.database.setup import Base, engine

def main_app():
    Base.metadata.create_all(engine)
    main()

if __name__ == "__main__":
    main_app()

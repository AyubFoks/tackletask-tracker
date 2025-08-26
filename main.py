from cli.commands import cli
from database.setup import Base, engine

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    cli()

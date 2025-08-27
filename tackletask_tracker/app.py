from .cli.commands import cli
from .database.setup import Base, engine

def main():
    Base.metadata.create_all(engine)
    cli()

if __name__ == "__main__":
    main()
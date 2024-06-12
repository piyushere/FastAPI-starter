from .todo import Todo
from sqlmodel import SQLModel


def generate_models(engine):
    SQLModel.metadata.create_all(engine)

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import create_engine
import os

sqlitePath = f"{os.path.abspath('')}/src/todos.sqlite3"
sync_engine = create_engine('sqlite:///' + sqlitePath)
async_engine = create_async_engine('sqlite+aiosqlite:///' + sqlitePath)

"""Banco — engine e sessão. Usa SQLite por padrão; troque via DATABASE_URL
(ex.: Postgres/Supabase) sem mudar o resto do código."""
import os
from sqlmodel import create_engine, SQLModel, Session

_DEFAULT = "sqlite:///" + os.path.join(os.path.dirname(__file__), "..", "plataforma.db")
DATABASE_URL = os.getenv("DATABASE_URL", _DEFAULT)
_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=_args)


def init_db():
    import app.models  # garante que as tabelas sejam registradas
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as s:
        yield s

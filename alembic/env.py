from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy import pool

from alembic import context
from app.config import settings
from app.models import SQLModel


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.build_url())
target_metadata = SQLModel.metadata

sync_engine = create_engine(
    settings.build_url(),
    poolclass=pool.NullPool,
)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    with sync_engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=SQLModel.metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

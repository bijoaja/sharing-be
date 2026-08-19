import asyncio
import re
from logging.config import fileConfig
from urllib.parse import urlsplit, urlunsplit

from sqlalchemy import pool, text
from sqlalchemy.ext.asyncio import async_engine_from_config, create_async_engine

from alembic import context

from app.config.settings import settings
from app.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Alembic migrations only manage the database itself (CREATE DATABASE) and
# granting privileges to the app user, not the `posts` table (created
# manually via scripts/create_posts_table.sql).
_DATABASE_URL = settings.DATABASE_URL
_DB_NAME = _DATABASE_URL.rsplit("/", 1)[-1]

_parts = urlsplit(_DATABASE_URL)
_APP_USER = _parts.username

# Root URL: same host/port as DATABASE_URL but authenticated as root, no
# default database selected (the database may not exist yet on first run).
_root_netloc = re.sub(r"^[^@]*@", f"root:{settings.MYSQL_ROOT_PASSWORD}@", _parts.netloc)
_ROOT_URL = urlunsplit((_parts.scheme, _root_netloc, "/", "", ""))

# Note: sqlalchemy.url is NOT set here globally (config.set_main_option)
# to avoid Alembic attempting to connect before bootstrapping is complete.



async def _bootstrap_database_and_grants() -> None:
    """Bootstrap step run as root (no default db selected), since the
    `article` database may not exist yet on first run: create the database,
    then grant the app user (DATABASE_URL) privileges on it. Alembic's own
    version tracking table lives inside that database, so this must run
    before the real migration context connects as the app user.
    """
    engine = create_async_engine(_ROOT_URL, poolclass=pool.NullPool)
    async with engine.connect() as connection:
        await connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {_DB_NAME}"))
        if _APP_USER and _APP_USER != "root":
            await connection.execute(
                text(f"CREATE USER IF NOT EXISTS '{_APP_USER}'@'%' IDENTIFIED BY '{settings.MYSQL_PASSWORD}'")
            )
            await connection.execute(
                text(f"GRANT ALL PRIVILEGES ON {_DB_NAME}.* TO '{_APP_USER}'@'%'")
            )
            await connection.execute(text("FLUSH PRIVILEGES"))
        await connection.commit()
    await engine.dispose()


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


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    await _bootstrap_database_and_grants()

    # Configure connection dynamically now that DB/user exist
    connectable = create_async_engine(_DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# This is the path to your Flask application, adjust as needed
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

# Import your application's database models and configuration
from app import create_app
from app.models import db  # Adjust based on your application structure

app = create_app()
app.app_context().push()

# Ensure the application is properly configured
config = context.config
config.set_main_option('sqlalchemy.url', app.config['SQLALCHEMY_DATABASE_URI'])

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Add your model metadata here (if you have multiple databases with different URLs, etc.)
# `target_metadata = your_model.Base.metadata`
target_metadata = db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

from sqlalchemy import exc

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = db.engine  # Assuming `db` is your SQLAlchemy database object

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        try:
            with context.begin_transaction():
                context.run_migrations()
        except exc.SQLAlchemyError as e:
            print(f"Error in SQLAlchemy migration: {e}")

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

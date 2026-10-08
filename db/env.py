from alembic import context

from api.config.banco import engine
from api.model import Base

with engine.connect() as conexao:
    context.configure(connection=conexao, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()

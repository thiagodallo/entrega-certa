# CAMADA: Config
# RESPONSABILIDADE: aplicar as migrations quando a API sobe e conferir se cada
#                   entidade bate com a sua tabela.
# SITUAÇÃO: implementada.
from pathlib import Path

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext

from api.config.banco import engine
from api.model import Base

RAIZ_DO_PROJETO = Path(__file__).resolve().parents[2]


def aplicar_migrations() -> None:
    configuracao = Config(toml_file=RAIZ_DO_PROJETO / "pyproject.toml")
    command.upgrade(configuracao, "head")


def validar_entidades() -> None:
    with engine.connect() as conexao:
        diferencas = compare_metadata(MigrationContext.configure(conexao), Base.metadata)
    if diferencas:
        raise RuntimeError(f"As entidades não batem com as tabelas do banco: {diferencas}")

# CAMADA: Config
# RESPONSABILIDADE: abrir a conexão com o PostgreSQL e entregar uma sessão por requisição.
# SITUAÇÃO: implementada.
import os
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

URL_DO_BANCO = os.getenv(
    "DATABASE_URL",
    "postgresql+pg8000://entrega_certa:entrega_certa@localhost:5437/entrega_certa",
)

engine = create_engine(URL_DO_BANCO, echo=True)
fabrica_de_sessoes = sessionmaker(bind=engine, expire_on_commit=False)


def obter_sessao() -> Iterator[Session]:
    with fabrica_de_sessoes() as sessao:
        yield sessao

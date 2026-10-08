# CAMADA: Model
# RESPONSABILIDADE: classe-mãe de todas as entidades. É por ela que o SQLAlchemy
#                   sabe quais tabelas o código espera encontrar no banco.
# SITUAÇÃO: implementada.
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

# CAMADA: Model
# RESPONSABILIDADE: entidade Turma, um grupo de alunos de uma disciplina.
#                   Representa a tabela turmas, criada em V1__criar_turmas.py.
# SITUAÇÃO: implementada.
from sqlalchemy import BigInteger, Identity, String
from sqlalchemy.orm import Mapped, mapped_column

from api.model.base import Base


class Turma(Base):
    __tablename__ = "turmas"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    disciplina: Mapped[str] = mapped_column(String(100))

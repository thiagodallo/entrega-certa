# CAMADA: Model
# RESPONSABILIDADE: entidade Aluno, quem entrega os trabalhos. Representa a
#                   tabela alunos, criada em V2__criar_alunos.py. Cada aluno
#                   pertence a uma turma (chave estrangeira turma_id).
# SITUAÇÃO: implementada.
from sqlalchemy import BigInteger, ForeignKey, Identity, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.model.base import Base
from api.model.turma import Turma


class Aluno(Base):
    __tablename__ = "alunos"
    __table_args__ = (UniqueConstraint("email", name="uk_alunos_email"),)

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    nome: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id"))
    turma: Mapped[Turma] = relationship()

# CAMADA: Model
# RESPONSABILIDADE: entidade Atividade, um trabalho com prazo e nota máxima
#                   passado para uma turma. Representa a tabela atividades,
#                   criada em V3__criar_atividades.py (chave estrangeira turma_id).
# SITUAÇÃO: implementada.
from datetime import date
from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey, Identity, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.model.base import Base
from api.model.turma import Turma


class Atividade(Base):
    __tablename__ = "atividades"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255))
    descricao: Mapped[str | None] = mapped_column(Text)
    prazo: Mapped[date]
    nota_maxima: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    turma_id: Mapped[int] = mapped_column(ForeignKey("turmas.id"))
    turma: Mapped[Turma] = relationship()

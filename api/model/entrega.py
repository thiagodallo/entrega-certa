# CAMADA: Model
# RESPONSABILIDADE: entidade Entrega, o envio de um aluno para uma atividade.
#                   Representa a tabela entregas, criada em V4__criar_entregas.py,
#                   com as chaves estrangeiras atividade_id e aluno_id e a
#                   unicidade da dupla (uma entrega por aluno em cada atividade).
# SITUAÇÃO: implementada.
from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey, Identity, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.model.aluno import Aluno
from api.model.atividade import Atividade
from api.model.base import Base


class Entrega(Base):
    __tablename__ = "entregas"
    __table_args__ = (
        UniqueConstraint("atividade_id", "aluno_id", name="uk_entregas_atividade_aluno"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    atividade_id: Mapped[int] = mapped_column(ForeignKey("atividades.id"))
    atividade: Mapped[Atividade] = relationship()
    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id"))
    aluno: Mapped[Aluno] = relationship()
    link: Mapped[str] = mapped_column(String(500))
    entregue_em: Mapped[datetime]
    atrasada: Mapped[bool]
    nota_teto: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    nota: Mapped[Decimal | None] = mapped_column(Numeric(4, 2))
    corrigida_em: Mapped[datetime | None]
# CAMADA: Repository
# RESPONSABILIDADE: ler e gravar turmas no banco. Só o Service chama esta classe.
# ROTAS ATENDIDAS: as de /turmas em docs/contrato-da-api.md.
# SITUAÇÃO: implementada.
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.config.banco import obter_sessao
from api.model.turma import Turma


class TurmaRepository:
    def __init__(self, sessao: Annotated[Session, Depends(obter_sessao)]):
        self.sessao = sessao

    def save(self, turma: Turma) -> Turma:
        self.sessao.add(turma)
        self.sessao.commit()
        return turma

    def find_by_id(self, turma_id: int) -> Turma | None:
        return self.sessao.get(Turma, turma_id)

    def find_all(self) -> list[Turma]:
        return list(self.sessao.scalars(select(Turma).order_by(Turma.id)))

# CAMADA: Repository
# RESPONSABILIDADE: ler e gravar atividades no banco. Só o Service chama esta classe.
# ROTAS ATENDIDAS: as de /atividades em docs/contrato-da-api.md, e POST /entregas,
#                  que busca a atividade pelo id.
# SITUAÇÃO: implementada.
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.config.banco import obter_sessao
from api.model.atividade import Atividade


class AtividadeRepository:
    def __init__(self, sessao: Annotated[Session, Depends(obter_sessao)]):
        self.sessao = sessao

    def save(self, atividade: Atividade) -> Atividade:
        self.sessao.add(atividade)
        self.sessao.commit()
        return atividade

    def find_by_id(self, atividade_id: int) -> Atividade | None:
        return self.sessao.get(Atividade, atividade_id)

    def find_all(self) -> list[Atividade]:
        return list(self.sessao.scalars(select(Atividade).order_by(Atividade.id)))

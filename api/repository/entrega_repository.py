# CAMADA: Repository
# RESPONSABILIDADE: ler e gravar entregas no banco. Só o Service chama esta classe.
#                   A consulta por atividade e aluno é a que sustenta a R3.
# ROTAS ATENDIDAS: as de /entregas em docs/contrato-da-api.md.
# SITUAÇÃO: implementada.
from typing import Annotated

from fastapi import Depends
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from api.config.banco import obter_sessao
from api.model.entrega import Entrega


class EntregaRepository:
    def __init__(self, sessao: Annotated[Session, Depends(obter_sessao)]):
        self.sessao = sessao

    def save(self, entrega: Entrega) -> Entrega:
        self.sessao.add(entrega)
        self.sessao.commit()
        return entrega

    def find_by_id(self, entrega_id: int) -> Entrega | None:
        return self.sessao.get(Entrega, entrega_id)

    def find_all(self) -> list[Entrega]:
        return list(self.sessao.scalars(select(Entrega).order_by(Entrega.id)))

    def exists_by_atividade_id_and_aluno_id(self, atividade_id: int, aluno_id: int) -> bool:
        consulta = select(
            exists().where(Entrega.atividade_id == atividade_id, Entrega.aluno_id == aluno_id)
        )
        return bool(self.sessao.scalar(consulta))
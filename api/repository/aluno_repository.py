# CAMADA: Repository
# RESPONSABILIDADE: ler e gravar alunos no banco. Só o Service chama esta classe.
# ROTAS ATENDIDAS: as de /alunos em docs/contrato-da-api.md, e POST /entregas,
#                  que busca o aluno pelo id.
# SITUAÇÃO: implementada.
from typing import Annotated

from fastapi import Depends
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from api.config.banco import obter_sessao
from api.model.aluno import Aluno


class AlunoRepository:
    def __init__(self, sessao: Annotated[Session, Depends(obter_sessao)]):
        self.sessao = sessao

    def save(self, aluno: Aluno) -> Aluno:
        self.sessao.add(aluno)
        self.sessao.commit()
        return aluno

    def find_by_id(self, aluno_id: int) -> Aluno | None:
        return self.sessao.get(Aluno, aluno_id)

    def find_all(self) -> list[Aluno]:
        return list(self.sessao.scalars(select(Aluno).order_by(Aluno.id)))

    def exists_by_email(self, email: str) -> bool:
        return bool(self.sessao.scalar(select(exists().where(Aluno.email == email))))

# CAMADA: Mapper
# RESPONSABILIDADE: converter AlunoRequestDTO em Aluno e Aluno em AlunoResponseDTO.
#                   A turma chega pronta do Service: o Mapper não consulta o banco.
# ROTAS ATENDIDAS: as de /alunos em docs/contrato-da-api.md.
# SITUAÇÃO: implementada.
from typing import Annotated

from fastapi import Depends

from api.dto.aluno_request_dto import AlunoRequestDTO
from api.dto.aluno_response_dto import AlunoResponseDTO
from api.mapper.turma_mapper import TurmaMapper
from api.model.aluno import Aluno
from api.model.turma import Turma


class AlunoMapper:
    def __init__(self, turma_mapper: Annotated[TurmaMapper, Depends()]):
        self.turma_mapper = turma_mapper

    def to_entity(self, request: AlunoRequestDTO, turma: Turma) -> Aluno:
        return Aluno(nome=request.nome, email=request.email, turma=turma)

    def to_response(self, aluno: Aluno) -> AlunoResponseDTO:
        return AlunoResponseDTO(
            id=aluno.id,
            nome=aluno.nome,
            email=aluno.email,
            turma=self.turma_mapper.to_response(aluno.turma),
        )

    def to_response_list(self, alunos: list[Aluno]) -> list[AlunoResponseDTO]:
        return [self.to_response(aluno) for aluno in alunos]

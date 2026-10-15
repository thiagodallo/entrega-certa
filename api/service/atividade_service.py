# CAMADA: Service
# RESPONSABILIDADE: cadastrar atividades para uma turma.
# REGRAS: nenhuma regra numerada. Garante que a turma existe (404). O prazo e a
#         nota máxima gravados aqui são a base de R2 e R4 em EntregaService.
# ROTAS ATENDIDAS: POST /atividades e GET /atividades.
# SITUAÇÃO: implementada em parte. GET por id, PUT e DELETE de /atividades
#           entram na próxima etapa.
from typing import Annotated

from fastapi import Depends

from api.dto.atividade_request_dto import AtividadeRequestDTO
from api.dto.atividade_response_dto import AtividadeResponseDTO
from api.mapper.atividade_mapper import AtividadeMapper
from api.repository.atividade_repository import AtividadeRepository
from api.repository.turma_repository import TurmaRepository
from api.service.turma_nao_encontrada_exception import TurmaNaoEncontradaException


class AtividadeService:
    def __init__(
        self,
        repository: Annotated[AtividadeRepository, Depends()],
        turma_repository: Annotated[TurmaRepository, Depends()],
        mapper: Annotated[AtividadeMapper, Depends()],
    ):
        self.repository = repository
        self.turma_repository = turma_repository
        self.mapper = mapper

    def criar(self, request: AtividadeRequestDTO) -> AtividadeResponseDTO:
        turma = self.turma_repository.find_by_id(request.turma_id)
        if turma is None:
            raise TurmaNaoEncontradaException(request.turma_id)
        atividade = self.repository.save(self.mapper.to_entity(request, turma))
        return self.mapper.to_response(atividade)

    def listar(self) -> list[AtividadeResponseDTO]:
        return self.mapper.to_response_list(self.repository.find_all())

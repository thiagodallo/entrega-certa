# CAMADA: Service
# RESPONSABILIDADE: cadastrar, listar e buscar turmas. É a API simples do projeto.
# REGRAS: nenhuma regra de negócio numerada. Lança TurmaNaoEncontradaException
#         quando o id não existe.
# ROTAS ATENDIDAS: POST /turmas, GET /turmas e GET /turmas/{id}.
# SITUAÇÃO: implementada. PUT e DELETE entram na próxima etapa.
from typing import Annotated

from fastapi import Depends

from api.dto.turma_request_dto import TurmaRequestDTO
from api.dto.turma_response_dto import TurmaResponseDTO
from api.mapper.turma_mapper import TurmaMapper
from api.repository.turma_repository import TurmaRepository
from api.service.turma_nao_encontrada_exception import TurmaNaoEncontradaException


class TurmaService:
    def __init__(
        self,
        repository: Annotated[TurmaRepository, Depends()],
        mapper: Annotated[TurmaMapper, Depends()],
    ):
        self.repository = repository
        self.mapper = mapper

    def criar(self, request: TurmaRequestDTO) -> TurmaResponseDTO:
        turma = self.repository.save(self.mapper.to_entity(request))
        return self.mapper.to_response(turma)

    def listar(self) -> list[TurmaResponseDTO]:
        return self.mapper.to_response_list(self.repository.find_all())

    def buscar_por_id(self, turma_id: int) -> TurmaResponseDTO:
        turma = self.repository.find_by_id(turma_id)
        if turma is None:
            raise TurmaNaoEncontradaException(turma_id)
        return self.mapper.to_response(turma)

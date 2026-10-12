# CAMADA: Mapper
# RESPONSABILIDADE: converter AtividadeRequestDTO em Atividade e Atividade em
#                   AtividadeResponseDTO. A turma chega pronta do Service.
# ROTAS ATENDIDAS: as de /atividades em docs/contrato-da-api.md.
# SITUAÇÃO: implementada.
from typing import Annotated

from fastapi import Depends

from api.dto.atividade_request_dto import AtividadeRequestDTO
from api.dto.atividade_response_dto import AtividadeResponseDTO
from api.mapper.turma_mapper import TurmaMapper
from api.model.atividade import Atividade
from api.model.turma import Turma


class AtividadeMapper:
    def __init__(self, turma_mapper: Annotated[TurmaMapper, Depends()]):
        self.turma_mapper = turma_mapper

    def to_entity(self, request: AtividadeRequestDTO, turma: Turma) -> Atividade:
        return Atividade(
            titulo=request.titulo,
            descricao=request.descricao,
            prazo=request.prazo,
            nota_maxima=request.nota_maxima,
            turma=turma,
        )

    def to_response(self, atividade: Atividade) -> AtividadeResponseDTO:
        return AtividadeResponseDTO(
            id=atividade.id,
            titulo=atividade.titulo,
            descricao=atividade.descricao,
            prazo=atividade.prazo,
            nota_maxima=float(atividade.nota_maxima),
            turma=self.turma_mapper.to_response(atividade.turma),
        )

    def to_response_list(self, atividades: list[Atividade]) -> list[AtividadeResponseDTO]:
        return [self.to_response(atividade) for atividade in atividades]

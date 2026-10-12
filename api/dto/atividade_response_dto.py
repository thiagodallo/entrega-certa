# CAMADA: DTO
# RESPONSABILIDADE: o que a API devolve sobre uma atividade. A turma sai como objeto.
# ROTAS ATENDIDAS: as de /atividades em docs/contrato-da-api.md.
# SITUAÇÃO: implementada.
from datetime import date

from pydantic import Field

from api.dto.base_dto import BaseDTO
from api.dto.turma_response_dto import TurmaResponseDTO


class AtividadeResponseDTO(BaseDTO):
    id: int = Field(examples=[1])
    titulo: str = Field(examples=["API REST de tarefas"])
    descricao: str | None = Field(examples=["CRUD em camadas, com Swagger"])
    prazo: date = Field(examples=["2026-10-15"])
    nota_maxima: float = Field(examples=[10.0])
    turma: TurmaResponseDTO

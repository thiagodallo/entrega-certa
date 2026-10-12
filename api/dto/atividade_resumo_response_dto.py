# CAMADA: DTO
# RESPONSABILIDADE: a atividade resumida que sai dentro da resposta de uma
#                   entrega: o que basta para entender o prazo e a nota máxima.
# ROTAS ATENDIDAS: as de /entregas em docs/contrato-da-api.md.
# SITUAÇÃO: implementada.
from datetime import date

from pydantic import Field

from api.dto.base_dto import BaseDTO


class AtividadeResumoResponseDTO(BaseDTO):
    id: int = Field(examples=[1])
    titulo: str = Field(examples=["API REST de tarefas"])
    prazo: date = Field(examples=["2026-10-07"])
    nota_maxima: float = Field(examples=[10.0])
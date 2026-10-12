# CAMADA: DTO
# RESPONSABILIDADE: o que o cliente envia para cadastrar uma atividade, com as
#                   validações de formato. A turma entra como id (turmaId).
# ROTAS ATENDIDAS: POST /atividades.
# SITUAÇÃO: implementada.
from datetime import date
from decimal import Decimal

from pydantic import Field

from api.dto.base_dto import BaseDTO


class AtividadeRequestDTO(BaseDTO):
    titulo: str = Field(min_length=1, max_length=255, examples=["API REST de tarefas"])
    descricao: str | None = Field(default=None, examples=["CRUD em camadas, com Swagger"])
    prazo: date = Field(examples=["2026-10-15"])
    nota_maxima: Decimal = Field(gt=0, max_digits=4, decimal_places=2, examples=[10])
    turma_id: int = Field(gt=0, examples=[1])
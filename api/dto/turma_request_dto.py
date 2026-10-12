# CAMADA: DTO
# RESPONSABILIDADE: o que o cliente envia para cadastrar uma turma, com as
#                   validações de formato.
# ROTAS ATENDIDAS: POST /turmas.
# SITUAÇÃO: implementada.
from pydantic import Field

from api.dto.base_dto import BaseDTO


class TurmaRequestDTO(BaseDTO):
    nome: str = Field(min_length=1, max_length=100, examples=["3ª fase noturno"])
    disciplina: str = Field(min_length=1, max_length=100, examples=["Backend"])

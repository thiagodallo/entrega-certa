# CAMADA: DTO
# RESPONSABILIDADE: o que a API devolve sobre uma turma.
# ROTAS ATENDIDAS: as de /turmas, e dentro das respostas de aluno e de atividade.
# SITUAÇÃO: implementada.
from pydantic import Field

from api.dto.base_dto import BaseDTO


class TurmaResponseDTO(BaseDTO):
    id: int = Field(examples=[1])
    nome: str = Field(examples=["3ª fase noturno"])
    disciplina: str = Field(examples=["Backend"])

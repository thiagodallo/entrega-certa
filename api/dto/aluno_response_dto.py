# CAMADA: DTO
# RESPONSABILIDADE: o que a API devolve sobre um aluno. A turma sai como objeto.
# ROTAS ATENDIDAS: as de /alunos em docs/contrato-da-api.md.
# SITUAÇÃO: implementada.
from pydantic import Field

from api.dto.base_dto import BaseDTO
from api.dto.turma_response_dto import TurmaResponseDTO

class AlunoResponseDTO(BaseDTO):
    id: int = Field(examples=[1])
    nome: str = Field(examples=["Ana Souza"])
    email: str = Field(examples=["ana.souza@email.com"])
    turma: TurmaResponseDTO

# CAMADA: DTO
# RESPONSABILIDADE: o aluno resumido que sai dentro da resposta de uma entrega.
#                   Não leva o e-mail nem a turma.
# ROTAS ATENDIDAS: as de /entregas em docs/contrato-da-api.md.
# SITUAÇÃO: implementada.
from pydantic import Field

from api.dto.base_dto import BaseDTO


class AlunoResumoResponseDTO(BaseDTO):
    id: int = Field(examples=[1])
    nome: str = Field(examples=["Ana Souza"])

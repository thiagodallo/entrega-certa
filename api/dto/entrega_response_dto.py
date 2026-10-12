# CAMADA: DTO
# RESPONSABILIDADE: o que a API devolve sobre uma entrega, com os campos que ela
#                   calcula: entregueEm, atrasada e notaTeto (R2), nota e
#                   corrigidaEm (R4).
# ROTAS ATENDIDAS: as de /entregas em docs/contrato-da-api.md.
# SITUAÇÃO: implementada.
from datetime import datetime

from pydantic import Field

from api.dto.aluno_resumo_response_dto import AlunoResumoResponseDTO
from api.dto.atividade_resumo_response_dto import AtividadeResumoResponseDTO
from api.dto.base_dto import BaseDTO


class EntregaResponseDTO(BaseDTO):
    id: int = Field(examples=[1])
    atividade: AtividadeResumoResponseDTO
    aluno: AlunoResumoResponseDTO
    link: str = Field(examples=["https://github.com/aluno/trabalho-api-rest"])
    entregue_em: datetime = Field(examples=["2026-10-08T19:30:00"])
    atrasada: bool = Field(examples=[True])
    nota_teto: float = Field(examples=[7.0])
    nota: float | None = Field(examples=[None])
    corrigida_em: datetime | None = Field(examples=[None])
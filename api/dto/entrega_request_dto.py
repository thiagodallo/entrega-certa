# CAMADA: DTO
# RESPONSABILIDADE: o que o cliente envia para registrar uma entrega. Só os ids
#                   e o link: a data, o atraso e o teto da nota quem decide é a API.
# ROTAS ATENDIDAS: POST /entregas.
# SITUAÇÃO: implementada.
from pydantic import Field

from api.dto.base_dto import BaseDTO


class EntregaRequestDTO(BaseDTO):
    atividade_id: int = Field(gt=0, examples=[1])
    aluno_id: int = Field(gt=0, examples=[1])
    link: str = Field(
        min_length=1,
        max_length=500,
        examples=["https://github.com/aluno/trabalho-api-rest"],
    )
# CAMADA: DTO
# RESPONSABILIDADE: o que o cliente envia para reenviar uma entrega: só o link
#                   novo. A data, o atraso e o teto são recalculados pela API.
# ROTAS ATENDIDAS: PUT /entregas/{id}/reenvio.
# SITUAÇÃO: implementada.
from pydantic import Field

from api.dto.base_dto import BaseDTO


class EntregaReenvioRequestDTO(BaseDTO):
    link: str = Field(
        min_length=1,
        max_length=500,
        examples=["https://github.com/aluno/trabalho-api-rest-v2"],
    )

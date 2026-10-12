# CAMADA: DTO
# RESPONSABILIDADE: o que o professor envia para corrigir uma entrega: a nota.
#                   Aqui só o formato é conferido; o teto da nota é a regra R4,
#                   que fica no EntregaService.
# ROTAS ATENDIDAS: PUT /entregas/{id}/correcao.
# SITUAÇÃO: implementada.
from decimal import Decimal

from pydantic import Field

from api.dto.base_dto import BaseDTO


class EntregaCorrecaoRequestDTO(BaseDTO):
    nota: Decimal = Field(ge=0, max_digits=4, decimal_places=2, examples=[8.5])

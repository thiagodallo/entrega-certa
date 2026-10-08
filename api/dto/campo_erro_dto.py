# CAMADA: DTO
# RESPONSABILIDADE: um erro de validação de um campo do corpo da requisição.
# SITUAÇÃO: implementada.
from pydantic import BaseModel, Field


class CampoErroDTO(BaseModel):
    campo: str = Field(description="Nome do campo no JSON", examples=["titulo"])
    mensagem: str = Field(
        description="Mensagem da validação que falhou",
        examples=["Título é obrigatório"],
    )

# CAMADA: DTO
# RESPONSABILIDADE: formato único de erro da API, usado em todo 400 e 404.
# SITUAÇÃO: implementada.
from datetime import datetime

from pydantic import BaseModel, Field

from api.dto.campo_erro_dto import CampoErroDTO


class ErroDTO(BaseModel):
    status: int = Field(description="Status HTTP", examples=[404])
    erro: str = Field(description="Nome do status HTTP", examples=["Not Found"])
    mensagem: str = Field(
        description="O que deu errado, em português",
        examples=["Turma não encontrada: 999"],
    )
    caminho: str = Field(description="Caminho da requisição", examples=["/turmas/999"])
    timestamp: datetime = Field(description="Momento do erro", examples=["2026-10-08T19:30:00"])
    campos: list[CampoErroDTO] = Field(
        description="Erros de validação por campo (vazio quando não se aplica)",
    )

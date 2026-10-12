# CAMADA: DTO
# RESPONSABILIDADE: o que o cliente envia para cadastrar um aluno, com as
#                   validações de formato. A turma entra como id (turmaId).
# ROTAS ATENDIDAS: POST /alunos.
# SITUAÇÃO: implementada.
from pydantic import Field

from api.dto.base_dto import BaseDTO

FORMATO_DE_EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class AlunoRequestDTO(BaseDTO):
    nome: str = Field(min_length=1, max_length=255, examples=["Ana Souza"])
    email: str = Field(
        max_length=255,
        pattern=FORMATO_DE_EMAIL,
        examples=["ana.souza@email.com"],
    )
    turma_id: int = Field(gt=0, examples=[1])

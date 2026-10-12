# CAMADA: Controller
# RESPONSABILIDADE: receber as requisições de /alunos, repassar ao AlunoService
#                   e devolver o DTO com o status certo.
# ROTAS ATENDIDAS: POST /alunos.
# SITUAÇÃO: implementada em parte. GET, PUT e DELETE de /alunos entram na
#           próxima etapa.
from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.dto.aluno_request_dto import AlunoRequestDTO
from api.dto.aluno_response_dto import AlunoResponseDTO
from api.dto.erro_dto import ErroDTO
from api.service.aluno_service import AlunoService

router = APIRouter(prefix="/alunos", tags=["Alunos"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um aluno em uma turma",
    responses={
        400: {"model": ErroDTO, "description": "Campo inválido ou e-mail já cadastrado"},
        404: {"model": ErroDTO, "description": "Turma não encontrada"},
    },
)
def criar(
    request: AlunoRequestDTO,
    service: Annotated[AlunoService, Depends()],
) -> AlunoResponseDTO:
    return service.criar(request)

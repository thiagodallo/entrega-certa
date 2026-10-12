# CAMADA: Controller
# RESPONSABILIDADE: receber as requisições de /atividades, repassar ao
#                   AtividadeService e devolver o DTO com o status certo.
# ROTAS ATENDIDAS: POST /atividades.
# SITUAÇÃO: implementada em parte. GET, PUT e DELETE de /atividades entram na
#           próxima etapa.
from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.dto.atividade_request_dto import AtividadeRequestDTO
from api.dto.atividade_response_dto import AtividadeResponseDTO
from api.dto.erro_dto import ErroDTO
from api.service.atividade_service import AtividadeService

router = APIRouter(prefix="/atividades", tags=["Atividades"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra uma atividade para uma turma",
    responses={
        400: {"model": ErroDTO, "description": "Campo inválido"},
        404: {"model": ErroDTO, "description": "Turma não encontrada"},
    },
)
def criar(
    request: AtividadeRequestDTO,
    service: Annotated[AtividadeService, Depends()],
) -> AtividadeResponseDTO:
    return service.criar(request)

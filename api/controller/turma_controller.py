# CAMADA: Controller
# RESPONSABILIDADE: receber as requisições de /turmas, repassar ao TurmaService
#                   e devolver o DTO com o status certo.
# ROTAS ATENDIDAS: POST /turmas, GET /turmas e GET /turmas/{id}.
# SITUAÇÃO: implementada. PUT e DELETE entram na próxima etapa.
from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.dto.erro_dto import ErroDTO
from api.dto.turma_request_dto import TurmaRequestDTO
from api.dto.turma_response_dto import TurmaResponseDTO
from api.service.turma_service import TurmaService

router = APIRouter(prefix="/turmas", tags=["Turmas"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra uma turma",
    responses={400: {"model": ErroDTO, "description": "Campo inválido"}},
)
def criar(
    request: TurmaRequestDTO,
    service: Annotated[TurmaService, Depends()],
) -> TurmaResponseDTO:
    return service.criar(request)


@router.get("", summary="Lista as turmas")
def listar(service: Annotated[TurmaService, Depends()]) -> list[TurmaResponseDTO]:
    return service.listar()


@router.get(
    "/{id}",
    summary="Busca uma turma pelo id",
    responses={404: {"model": ErroDTO, "description": "Turma não encontrada"}},
)
def buscar_por_id(id: int, service: Annotated[TurmaService, Depends()]) -> TurmaResponseDTO:
    return service.buscar_por_id(id)

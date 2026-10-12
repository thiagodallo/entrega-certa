# CAMADA: Controller
# RESPONSABILIDADE: receber as requisições de /entregas, repassar ao
#                   EntregaService e devolver o DTO com o status certo. Nenhuma
#                   regra é decidida aqui.
# ROTAS ATENDIDAS: POST /entregas, GET /entregas/{id}, PUT /entregas/{id}/reenvio
#                  e PUT /entregas/{id}/correcao.
# SITUAÇÃO: implementada. A listagem (GET /entregas) entra na próxima etapa.
from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.dto.entrega_correcao_request_dto import EntregaCorrecaoRequestDTO
from api.dto.entrega_reenvio_request_dto import EntregaReenvioRequestDTO
from api.dto.entrega_request_dto import EntregaRequestDTO
from api.dto.entrega_response_dto import EntregaResponseDTO
from api.dto.erro_dto import ErroDTO
from api.service.entrega_service import EntregaService

router = APIRouter(prefix="/entregas", tags=["Entregas"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Registra a entrega de um aluno (R1, R2 e R3)",
    responses={
        400: {"model": ErroDTO, "description": "Campo inválido ou regra R1, R2 ou R3 violada"},
        404: {"model": ErroDTO, "description": "Atividade ou aluno não encontrado"},
    },
)
def registrar(
    request: EntregaRequestDTO,
    service: Annotated[EntregaService, Depends()],
) -> EntregaResponseDTO:
    return service.registrar(request)


@router.get(
    "/{id}",
    summary="Busca uma entrega pelo id",
    responses={404: {"model": ErroDTO, "description": "Entrega não encontrada"}},
)
def buscar_por_id(id: int, service: Annotated[EntregaService, Depends()]) -> EntregaResponseDTO:
    return service.buscar_por_id(id)


@router.put(
    "/{id}/reenvio",
    summary="Troca o link de uma entrega ainda não corrigida (R2 e R3)",
    responses={
        400: {"model": ErroDTO, "description": "Campo inválido ou regra R2 ou R3 violada"},
        404: {"model": ErroDTO, "description": "Entrega não encontrada"},
    },
)
def reenviar(
    id: int,
    request: EntregaReenvioRequestDTO,
    service: Annotated[EntregaService, Depends()],
) -> EntregaResponseDTO:
    return service.reenviar(id, request)


@router.put(
    "/{id}/correcao",
    summary="Lança a nota de uma entrega (R4)",
    responses={
        400: {"model": ErroDTO, "description": "Campo inválido ou regra R4 violada"},
        404: {"model": ErroDTO, "description": "Entrega não encontrada"},
    },
)
def corrigir(
    id: int,
    request: EntregaCorrecaoRequestDTO,
    service: Annotated[EntregaService, Depends()],
) -> EntregaResponseDTO:
    return service.corrigir(id, request)

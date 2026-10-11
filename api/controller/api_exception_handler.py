# CAMADA: Controller
# RESPONSABILIDADE: transformar os erros da API em respostas 400 e 404, sempre
#                   no formato ErroDTO.
# SITUAÇÃO: implementada.
from datetime import datetime
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from api.dto.campo_erro_dto import CampoErroDTO
from api.dto.erro_dto import ErroDTO
from api.service.recurso_nao_encontrado_exception import RecursoNaoEncontradoException
from api.service.regra_de_negocio_exception import RegraDeNegocioException

MENSAGEM_CORPO_ILEGIVEL = (
    "Corpo da requisição inválido: confira o JSON e o formato das datas (yyyy-MM-dd)"
)
MENSAGEM_DADOS_INVALIDOS = "Dados inválidos: confira a lista de campos"

MENSAGENS_DE_VALIDACAO = {
    "missing": "Campo obrigatório",
    "string_too_short": "Texto curto demais ou vazio",
    "string_too_long": "Texto longo demais",
    "string_pattern_mismatch": "Formato inválido",
    "greater_than": "Valor abaixo do mínimo permitido",
    "greater_than_equal": "Valor abaixo do mínimo permitido",
    "less_than": "Valor acima do máximo permitido",
    "less_than_equal": "Valor acima do máximo permitido",
    "int_parsing": "Precisa ser um número inteiro",
    "decimal_parsing": "Precisa ser um número",
    "decimal_max_digits": "Número grande demais",
    "decimal_max_places": "Use no máximo duas casas decimais",
    "decimal_whole_digits": "Número grande demais",
    "date_from_datetime_parsing": "Data inválida, use yyyy-MM-dd",
    "datetime_from_date_parsing": "Data e hora inválidas, use yyyy-MM-ddTHH:mm:ss",
}


def responder(
    status: HTTPStatus,
    mensagem: str,
    request: Request,
    campos: list[CampoErroDTO] | None = None,
) -> JSONResponse:
    erro = ErroDTO(
        status=status.value,
        erro=status.phrase,
        mensagem=mensagem,
        caminho=request.url.path,
        timestamp=datetime.now().replace(microsecond=0),
        campos=campos or [],
    )
    return JSONResponse(status_code=status.value, content=jsonable_encoder(erro))


def tratar_nao_encontrado(request: Request, erro: RecursoNaoEncontradoException) -> JSONResponse:
    return responder(HTTPStatus.NOT_FOUND, erro.mensagem, request)


def tratar_regra_de_negocio(request: Request, erro: RegraDeNegocioException) -> JSONResponse:
    return responder(HTTPStatus.BAD_REQUEST, erro.mensagem, request)


def converter_campo(detalhe: dict) -> CampoErroDTO:
    campo = ".".join(str(parte) for parte in detalhe["loc"][1:])
    mensagem = MENSAGENS_DE_VALIDACAO.get(detalhe["type"], detalhe["msg"])
    return CampoErroDTO(campo=campo, mensagem=mensagem)


def tratar_validacao(request: Request, erro: RequestValidationError) -> JSONResponse:
    detalhes = erro.errors()
    if any(detalhe["type"] == "json_invalid" for detalhe in detalhes):
        return responder(HTTPStatus.BAD_REQUEST, MENSAGEM_CORPO_ILEGIVEL, request)
    campos = sorted(
        (converter_campo(detalhe) for detalhe in detalhes),
        key=lambda campo: (campo.campo, campo.mensagem),
    )
    return responder(HTTPStatus.BAD_REQUEST, MENSAGEM_DADOS_INVALIDOS, request, campos)


def tratar_erro_http(request: Request, erro: HTTPException) -> JSONResponse:
    status = HTTPStatus(erro.status_code)
    return responder(status, str(erro.detail), request)


def registrar_tratadores_de_erro(app: FastAPI) -> None:
    app.add_exception_handler(RecursoNaoEncontradoException, tratar_nao_encontrado)
    app.add_exception_handler(RegraDeNegocioException, tratar_regra_de_negocio)
    app.add_exception_handler(RequestValidationError, tratar_validacao)
    app.add_exception_handler(HTTPException, tratar_erro_http)
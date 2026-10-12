# CAMADA: Aplicação
# RESPONSABILIDADE: ponto de entrada. Cria a API, aplica as migrations na subida,
#                   liga os tratadores de erro e os Controllers e serve o painel
#                   de demonstração (pasta web) em /painel.
# SITUAÇÃO: implementada.
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.config.migracoes import aplicar_migrations, validar_entidades
from api.config.openapi_config import INFORMACOES_DA_API
from api.controller import (
    aluno_controller,
    atividade_controller,
    entrega_controller,
    turma_controller,
)
from api.controller.api_exception_handler import registrar_tratadores_de_erro

PASTA_DO_PAINEL = Path(__file__).resolve().parent.parent / "web"


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI) -> AsyncIterator[None]:
    aplicar_migrations()
    validar_entidades()
    yield


app = FastAPI(lifespan=ciclo_de_vida, **INFORMACOES_DA_API)
registrar_tratadores_de_erro(app)
app.include_router(turma_controller.router)
app.include_router(aluno_controller.router)
app.include_router(atividade_controller.router)
app.include_router(entrega_controller.router)
app.mount("/painel", StaticFiles(directory=PASTA_DO_PAINEL, html=True), name="painel")

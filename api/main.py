# CAMADA: Aplicação
# RESPONSABILIDADE: ponto de entrada. Cria a API, aplica as migrations na subida
#                   e liga os tratadores de erro e os Controllers.
# SITUAÇÃO: implementada.
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.config.migracoes import aplicar_migrations, validar_entidades
from api.config.openapi_config import INFORMACOES_DA_API
from api.controller import aluno_controller, turma_controller
from api.controller.api_exception_handler import registrar_tratadores_de_erro


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI) -> AsyncIterator[None]:
    aplicar_migrations()
    validar_entidades()
    yield


app = FastAPI(lifespan=ciclo_de_vida, **INFORMACOES_DA_API)
registrar_tratadores_de_erro(app)
app.include_router(turma_controller.router)
app.include_router(aluno_controller.router)

# CAMADA: Config
# RESPONSABILIDADE: título, versão e descrição que aparecem no topo do Swagger UI,
#                   nos mesmos endereços do template da disciplina. Também troca,
#                   na documentação, o 422 que o FastAPI anuncia por padrão pelo
#                   400 que a API devolve de verdade nos erros de validação.
# SITUAÇÃO: implementada.
from fastapi import FastAPI

INFORMACOES_DA_API = {
    "title": "Projeto Final - Entrega Certa",
    "version": "Etapa 1",
    "description": (
        "API REST do Projeto Final da disciplina de Backend (SATC). "
        "Controla as entregas de atividades com prazo de uma turma. "
        "Todo corpo de requisição e de resposta é um **DTO** "
        "e todo erro 400/404 sai no formato `ErroDTO`."
    ),
    "docs_url": "/swagger-ui.html",
    "openapi_url": "/v3/api-docs",
    "redoc_url": None,
}

RESPOSTA_DE_VALIDACAO = {
    "description": "Campo inválido",
    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErroDTO"}}},
}
ESQUEMAS_DO_422 = ("HTTPValidationError", "ValidationError")


def documentar_validacao_como_400(app: FastAPI) -> None:
    gerar_documentacao = app.openapi

    def gerar_documentacao_sem_422() -> dict:
        documentacao = gerar_documentacao()
        for rota in documentacao.get("paths", {}).values():
            for operacao in rota.values():
                if operacao["responses"].pop("422", None):
                    operacao["responses"].setdefault("400", RESPOSTA_DE_VALIDACAO)
        esquemas = documentacao.get("components", {}).get("schemas", {})
        for nome in ESQUEMAS_DO_422:
            esquemas.pop(nome, None)
        return documentacao

    app.openapi = gerar_documentacao_sem_422
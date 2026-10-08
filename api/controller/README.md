# controller: a porta de entrada da API

É aqui que a requisição HTTP chega. O Controller recebe o pedido, repassa para o Service e devolve a resposta.

**Nesta etapa:** crie um Controller para cada entidade. Precisam ter rotas o da API simples (`POST`, `GET` e `GET /{id}`) e os que as regras de negócio usam. Os outros ficam montados: o arquivo criado, com o `router` e o comentário no topo dizendo quais rotas vai atender.

Cada Controller é um arquivo com um `router`:

```python
router = APIRouter(prefix="/turmas", tags=["Turmas"])
```

O `router` precisa ser registrado em `api/main.py` com `app.include_router(...)`.

| Faz | Não faz |
|---|---|
| Liga verbo e caminho a uma função (`@router.get`, `@router.post`...) | Regra de negócio |
| Recebe o DTO de entrada já validado | Acessar o Repository |
| Escolhe o status HTTP (`200`, `201`, `204`) | Importar qualquer classe de `api.model` |
| Descreve a rota para o Swagger (`summary`, `responses`) | Montar resposta de erro: isso é do `api_exception_handler.py` |

**Já vem pronto:** `api_exception_handler.py`, que transforma os erros em `400` e `404` no formato único. Equivale ao `ApiExceptionHandler` do template em Java.

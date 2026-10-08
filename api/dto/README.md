# dto: o JSON que entra e o que sai

Um DTO descreve o formato do JSON de uma rota. É o que o cliente da API enxerga; a entidade fica escondida atrás dele.

**Nesta etapa:** crie o DTO de entrada e o de saída de todas as entidades, com os campos e as validações de `docs/contrato-da-api.md`.

| DTO | Para que serve | Exemplo |
|---|---|---|
| `...RequestDTO` | O que o cliente pode enviar. É onde ficam as validações (`Field(min_length=1)`, `Field(gt=0)`...) | `TurmaRequestDTO` |
| `...ResponseDTO` | O que a API devolve. Inclui o `id` e os campos que a API calcula | `TurmaResponseDTO` |

- Cada DTO é um modelo do Pydantic (`BaseModel`), o equivalente ao `record` do Java.
- Nada de SQLAlchemy aqui, e nenhuma entidade como campo de um DTO.
- Relacionamento entra como id (`"turmaId": 1`) e sai como objeto (`"turma": {...}`).

**Já vem pronto:** `ErroDTO` e `CampoErroDTO`, o formato único de erro.

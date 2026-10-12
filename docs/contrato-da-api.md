# Contrato da API

O contrato é o que o cliente da API enxerga: rotas, JSON e status.

> Primeira versão, feita na Aula 10. Nenhuma rota responde ainda. A coluna **Funciona** mostra o plano: `Etapa 1` para as rotas da API simples e as que as regras de negócio usam, `depois` para as demais. Na entrega ela passa a dizer `sim` ou `não`.

## Convenções

| Item | Valor |
|---|---|
| Endereço base | `http://localhost:8000` |
| Formato | JSON, na requisição e na resposta, com campos em `camelCase` |
| Datas | `yyyy-MM-dd` |
| Data e hora | `yyyy-MM-ddTHH:mm:ss` |
| Erros | Sempre no formato `ErroDTO` (ver [Erros](#erros)) |
| Documentação viva | `http://localhost:8000/swagger-ui.html` |

## Rotas

### Turmas

A API simples do projeto.

| Verbo | Caminho | O que faz | Entrada | Saída | Sucesso | Erros | Funciona |
|---|---|---|---|---|---|---|---|
| `GET` | `/turmas` | Lista as turmas | Nenhuma | lista de `TurmaResponseDTO` | `200` | Nenhum | Etapa 1 |
| `GET` | `/turmas/{id}` | Busca uma turma | Nenhuma | `TurmaResponseDTO` | `200` | `404` | Etapa 1 |
| `POST` | `/turmas` | Cadastra uma turma | `TurmaRequestDTO` | `TurmaResponseDTO` | `201` | `400` | Etapa 1 |
| `PUT` | `/turmas/{id}` | Atualiza uma turma | `TurmaRequestDTO` | `TurmaResponseDTO` | `200` | `400`, `404` | depois |
| `DELETE` | `/turmas/{id}` | Remove uma turma | Nenhuma | Nenhuma (sem corpo) | `204` | `404` | depois |

### Alunos

| Verbo | Caminho | O que faz | Entrada | Saída | Sucesso | Erros | Funciona |
|---|---|---|---|---|---|---|---|
| `POST` | `/alunos` | Cadastra um aluno em uma turma | `AlunoRequestDTO` | `AlunoResponseDTO` | `201` | `400`, `404` | Etapa 1 |
| `GET` | `/alunos` | Lista os alunos | Nenhuma | lista de `AlunoResponseDTO` | `200` | Nenhum | depois |
| `GET` | `/alunos/{id}` | Busca um aluno | Nenhuma | `AlunoResponseDTO` | `200` | `404` | depois |
| `PUT` | `/alunos/{id}` | Atualiza um aluno | `AlunoRequestDTO` | `AlunoResponseDTO` | `200` | `400`, `404` | depois |
| `DELETE` | `/alunos/{id}` | Remove um aluno | Nenhuma | Nenhuma (sem corpo) | `204` | `404` | depois |

### Atividades

| Verbo | Caminho | O que faz | Entrada | Saída | Sucesso | Erros | Funciona |
|---|---|---|---|---|---|---|---|
| `POST` | `/atividades` | Cadastra uma atividade para uma turma | `AtividadeRequestDTO` | `AtividadeResponseDTO` | `201` | `400`, `404` | Etapa 1 |
| `GET` | `/atividades` | Lista as atividades | Nenhuma | lista de `AtividadeResponseDTO` | `200` | Nenhum | depois |
| `GET` | `/atividades/{id}` | Busca uma atividade | Nenhuma | `AtividadeResponseDTO` | `200` | `404` | depois |
| `PUT` | `/atividades/{id}` | Atualiza uma atividade | `AtividadeRequestDTO` | `AtividadeResponseDTO` | `200` | `400`, `404` | depois |
| `DELETE` | `/atividades/{id}` | Remove uma atividade | Nenhuma | Nenhuma (sem corpo) | `204` | `404` | depois |

`POST /alunos` e `POST /atividades` entram na Etapa 1 porque as regras das entregas precisam de um aluno e de uma atividade cadastrados.

### Entregas

| Verbo | Caminho | O que faz | Entrada | Saída | Sucesso | Erros | Funciona |
|---|---|---|---|---|---|---|---|
| `GET` | `/entregas` | Lista as entregas | Nenhuma | lista de `EntregaResponseDTO` | `200` | Nenhum | depois |
| `GET` | `/entregas/{id}` | Busca uma entrega | Nenhuma | `EntregaResponseDTO` | `200` | `404` | Etapa 1 |

### Rotas que não são CRUD

As que nascem das regras de negócio do README.

| Verbo | Caminho | O que faz | Regra | Sucesso | Erros |
|---|---|---|---|---|---|
| `POST` | `/entregas` | Registra a entrega de um aluno, calcula se está atrasada e qual é o teto da nota | R1, R2 e R3 | `201` | `400`, `404` |
| `PUT` | `/entregas/{id}/reenvio` | Troca o link de uma entrega ainda não corrigida e recalcula atraso e teto | R2 e R3 | `200` | `400`, `404` |
| `PUT` | `/entregas/{id}/correcao` | Lança a nota da entrega | R4 | `200` | `400`, `404` |

## DTOs

O que entra não é igual ao que sai: o cliente não envia `id` nem campos que a API decide.

| DTO | Direção | Campos | Validações |
|---|---|---|---|
| `TurmaRequestDTO` | entrada | `nome`, `disciplina` | Os dois obrigatórios, até 100 caracteres |
| `TurmaResponseDTO` | saída | `id`, `nome`, `disciplina` | Nenhuma |
| `AlunoRequestDTO` | entrada | `nome`, `email`, `turmaId` | Os três obrigatórios; `nome` e `email` até 255 caracteres; `email` em formato de e-mail |
| `AlunoResponseDTO` | saída | `id`, `nome`, `email`, `turma` | Nenhuma |
| `AtividadeRequestDTO` | entrada | `titulo`, `descricao`, `prazo`, `notaMaxima`, `turmaId` | `descricao` opcional; `titulo` até 255 caracteres; `notaMaxima` maior que zero, até 99.99, com no máximo duas casas |
| `AtividadeResponseDTO` | saída | `id`, `titulo`, `descricao`, `prazo`, `notaMaxima`, `turma` | Nenhuma |
| `EntregaRequestDTO` | entrada | `atividadeId`, `alunoId`, `link` | Os três obrigatórios; `link` até 500 caracteres |
| `EntregaReenvioRequestDTO` | entrada | `link` | Obrigatório, até 500 caracteres |
| `EntregaCorrecaoRequestDTO` | entrada | `nota` | Obrigatória, zero ou mais |
| `EntregaResponseDTO` | saída | `id`, `atividade`, `aluno`, `link`, `entregueEm`, `atrasada`, `notaTeto`, `nota`, `corrigidaEm` | Nenhuma |
| `AtividadeResumoResponseDTO` | saída, dentro de `EntregaResponseDTO` | `id`, `titulo`, `prazo`, `notaMaxima` | Nenhuma |
| `AlunoResumoResponseDTO` | saída, dentro de `EntregaResponseDTO` | `id`, `nome` | Nenhuma |

Como a R2 conta o atraso: vale o dia de `entregueEm`, no relógio do servidor. Entrega até o dia do prazo está em dia; no dia seguinte, até 23h59, entra como atrasada; do segundo dia em diante é recusada. O reenvio refaz essa conta com a data do reenvio.

## Exemplos

### `POST /turmas`

Requisição:

```json
{
  "nome": "3ª fase noturno",
  "disciplina": "Backend"
}
```

Resposta, `201 Created`:

```json
{
  "id": 1,
  "nome": "3ª fase noturno",
  "disciplina": "Backend"
}
```

### `POST /entregas`

Requisição, enviada um dia depois do prazo de uma atividade que vale 10:

```json
{
  "atividadeId": 1,
  "alunoId": 1,
  "link": "https://github.com/aluno/trabalho-api-rest"
}
```

Resposta, `201 Created`:

```json
{
  "id": 1,
  "atividade": { "id": 1, "titulo": "API REST de tarefas", "prazo": "2026-10-07", "notaMaxima": 10.0 },
  "aluno": { "id": 1, "nome": "Ana Souza" },
  "link": "https://github.com/aluno/trabalho-api-rest",
  "entregueEm": "2026-10-08T19:30:00",
  "atrasada": true,
  "notaTeto": 7.0,
  "nota": null,
  "corrigidaEm": null
}
```

## Erros

Todo erro sai no mesmo formato. Este é o `404` de `GET /turmas/999`:

```json
{
  "status": 404,
  "erro": "Not Found",
  "mensagem": "Turma não encontrada: 999",
  "caminho": "/turmas/999",
  "timestamp": "2026-10-08T19:30:00",
  "campos": []
}
```

No `400` de validação, a lista `campos` traz um item por campo inválido: `{"campo": "nome", "mensagem": "Campo obrigatório"}`.

| Status | Quando acontece neste projeto |
|---|---|
| `400` | JSON ilegível ou campo inválido no DTO de entrada |
| `404` | Id que não existe |
| `400` | Regra de negócio violada: a `mensagem` diz qual regra barrou o pedido |
| `400` | E-mail de aluno repetido em `POST /alunos`: `Já existe um aluno com este e-mail` |

Mensagens das regras:

| Regra | Mensagem |
|---|---|
| R1 | `R1: o aluno não pertence à turma desta atividade` |
| R2 | `R2: o prazo de entrega com atraso (1 dia) já terminou` |
| R3 | `R3: o aluno já tem uma entrega para esta atividade` e `R3: a entrega já foi corrigida e não pode ser reenviada` |
| R4 | `R4: a nota não pode passar do teto desta entrega` |

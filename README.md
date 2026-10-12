# Entrega Certa

API para o professor controlar as entregas de atividades de uma turma: quem entregou, quando entregou, se foi no prazo e qual nota cada entrega pode receber.

Projeto Final da disciplina de Backend (Engenharia de Software, SATC). **Etapa 1: arquitetura do backend.**

## Índice

- [Integrantes](#integrantes)
- [O problema](#o-problema)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Entidades](#entidades)
- [Rotas](#rotas)
- [Como executar](#como-executar)
- [Situação do projeto](#situação-do-projeto)
- [Documentação](#documentação)

## Integrantes

| Nome | GitHub |
|---|---|
| Thiago de Luca Dalló | [@thiagodallo](https://github.com/thiagodallo) |
| Murilo Claudio Cambruzzi | [@murilo-cbz](https://github.com/murilo-cbz) |
| Vinicius Fabris dos Santos | [@ViniciusFabris](https://github.com/ViniciusFabris) |

## O problema

**Tema sorteado:** Educação e Aprendizagem

Professores recebem trabalhos por e-mail e WhatsApp e perdem o controle de quem entregou e quando. A tolerância para atraso é aplicada de cabeça, de um jeito para cada aluno, e vira discussão na hora da nota. O Entrega Certa registra cada entrega com data e hora, aplica a mesma regra de atraso para todos e impede que um trabalho já corrigido seja trocado.

**Quem usa o sistema:**

| Quem | O que faz no sistema |
|---|---|
| Professor | Cadastra turmas, alunos e atividades, e corrige as entregas |
| Aluno | Envia e reenvia a entrega de cada atividade da sua turma |

**Regras de negócio.** O que o sistema garante ou impede:

| # | Regra | Onde está no código | Rota que usa |
|---|---|---|---|
| R1 | Só entrega uma atividade o aluno que pertence à turma dela | `EntregaService` | `POST /entregas` |
| R2 | Entrega até 1 dia depois do prazo é aceita, mas a nota fica limitada a 70% da nota máxima. Depois disso a entrega é recusada | `EntregaService` | `POST /entregas`, `PUT /entregas/{id}/reenvio` |
| R3 | Cada aluno tem uma única entrega por atividade. Pode reenviar enquanto ela não for corrigida; depois de corrigida, não | `EntregaService` | `POST /entregas`, `PUT /entregas/{id}/reenvio` |
| R4 | A nota da correção não pode passar do teto da entrega: a nota máxima da atividade, ou 70% dela quando a entrega foi atrasada | `EntregaService` | `PUT /entregas/{id}/correcao` |

**Fora do escopo:** login e perfis de acesso, envio de arquivos (a entrega é um link), aluno em mais de uma turma, notificações e cálculo de média final.

## Tecnologias

| O quê | Qual |
|---|---|
| Linguagem | Python 3.12 ou mais novo |
| Framework | FastAPI, com Pydantic para os DTOs e a validação |
| Acesso ao banco | SQLAlchemy 2.0, com o driver pg8000 |
| Banco de dados | PostgreSQL 16, em Docker |
| Migrations | Alembic |
| Documentação da API | Swagger UI, gerado pelo FastAPI |
| Dependências | uv |

### Python no lugar de Java

O template e os critérios da disciplina foram escritos para Java + Spring Boot. Este projeto mantém as mesmas camadas, os mesmos nomes de classe e os mesmos endereços, com as ferramentas equivalentes:

| Critério | No template (Java) | Neste projeto (Python) |
|---|---|---|
| P1 Sobe pelo README | `./mvnw spring-boot:run` | `uv run python -m uvicorn api.main:app --port 8000` |
| P2 Camadas | Pacotes em `src/main/java/api/` | Pastas em [`api/`](api): `controller`, `service`, `mapper`, `repository`, `model`, `dto`, `config` |
| P3 Banco e entidades | Flyway, `@Entity` e `ddl-auto=validate` | Alembic em [`db/migration`](db/migration), classes do SQLAlchemy em `api/model` e a conferência de [`api/config/migracoes.py`](api/config/migracoes.py), que impede a API de subir se a entidade não bater com a tabela |
| P4 DTOs | `record` com Bean Validation | Modelos do Pydantic em `api/dto` |
| P5 Estrutura | Injeção pelo construtor do Spring | Construtor com `Depends` do FastAPI. Comentário no topo de cada arquivo |
| P6 API simples | `@RestController`, `RecursoNaoEncontradoException` | `APIRouter`, e a mesma `RecursoNaoEncontradoException` em `api/service` |
| P7 e P8 Regras | `RegraDeNegocioException` no Service | A mesma `RegraDeNegocioException`, lançada no Service |
| Formato de erro | `ApiExceptionHandler`, `ErroDTO` | [`api_exception_handler.py`](api/controller/api_exception_handler.py), com o mesmo `ErroDTO` |
| Swagger | springdoc-openapi | FastAPI, nos mesmos caminhos `/swagger-ui.html` e `/v3/api-docs` |

## Arquitetura

A API é organizada em camadas. Uma requisição entra pelo Controller, passa pelo Service, que aplica as regras de negócio, e chega ao banco pelo Repository; a resposta faz o caminho de volta. O Mapper converte DTO em entidade e entidade em DTO.

**Mapa da estrutura.** Uma linha por entidade. Em cada célula, a classe e a situação: **pronta**, **implementada** (já tem lógica), **em parte** (só uma parte das rotas), **montada** (criada, ligada às outras, ainda sem lógica) ou **a criar**.

| Entidade | Migration | Model | Repository | DTOs | Mapper | Service | Controller |
|---|---|---|---|---|---|---|---|
| Turma | `V1__criar_turmas.py`, pronta | `Turma`, pronta | `TurmaRepository`, pronta | `TurmaRequestDTO`, `TurmaResponseDTO`, prontos | `TurmaMapper`, implementada | `TurmaService`, em parte (falta `PUT` e `DELETE`) | `turma_controller`, em parte (falta `PUT` e `DELETE`) |
| Aluno | `V2__criar_alunos.py`, pronta | `Aluno`, pronta | `AlunoRepository`, pronta | `AlunoRequestDTO`, `AlunoResponseDTO`, prontos | `AlunoMapper`, implementada | `AlunoService`, em parte (só o cadastro) | `aluno_controller`, em parte (só o `POST`) |
| Atividade | `V3__criar_atividades.py`, pronta | `Atividade`, pronta | `AtividadeRepository`, pronta | `AtividadeRequestDTO`, `AtividadeResponseDTO`, prontos | `AtividadeMapper`, implementada | `AtividadeService`, em parte (só o cadastro) | `atividade_controller`, em parte (só o `POST`) |
| Entrega | `V4__criar_entregas.py`, pronta | `Entrega`, pronta | `EntregaRepository`, pronta | `EntregaRequestDTO`, `EntregaReenvioRequestDTO`, `EntregaCorrecaoRequestDTO`, `EntregaResponseDTO`, `AtividadeResumoResponseDTO`, `AlunoResumoResponseDTO`, prontos | `EntregaMapper`, implementada | `EntregaService`, implementada (R1 a R4; falta só a listagem) | `entrega_controller`, implementada (falta só a listagem) |

Já existe o que não depende das entidades: a conexão com o banco, as migrations na subida, o Swagger e o formato único de erro.

## Entidades

| Entidade | O que representa | Como se relaciona |
|---|---|---|
| Turma | Um grupo de alunos de uma disciplina | Tem vários alunos e várias atividades |
| Aluno | Quem entrega os trabalhos | Pertence a uma turma e faz várias entregas |
| Atividade | Um trabalho com prazo e nota máxima | Pertence a uma turma e recebe várias entregas |
| Entrega | O envio de um aluno para uma atividade | Pertence a um aluno e a uma atividade |

Atributos, tipos e o diagrama das tabelas estão em [docs/modelo-de-dominio.md](docs/modelo-de-dominio.md).

## Rotas

### As que já funcionam

| Verbo | Caminho | O que faz | Sucesso | Erros |
|---|---|---|---|---|
| `POST` | `/turmas` | Cadastra uma turma | `201` | `400` |
| `GET` | `/turmas` | Lista as turmas | `200` | Nenhum |
| `GET` | `/turmas/{id}` | Busca uma turma | `200` | `404` |
| `POST` | `/alunos` | Cadastra um aluno em uma turma | `201` | `400`, `404` |
| `POST` | `/atividades` | Cadastra uma atividade para uma turma | `201` | `400`, `404` |
| `POST` | `/entregas` | Registra uma entrega, aplicando R1, R2 e R3 | `201` | `400`, `404` |
| `GET` | `/entregas/{id}` | Busca uma entrega | `200` | `404` |
| `PUT` | `/entregas/{id}/reenvio` | Troca o link de uma entrega não corrigida, aplicando R2 e R3 | `200` | `400`, `404` |
| `PUT` | `/entregas/{id}/correcao` | Lança a nota da entrega, aplicando R4 | `200` | `400`, `404` |

### Erros

Todo erro sai no mesmo formato. Este é o `400` de uma regra de negócio violada:

```json
{
  "status": 400,
  "erro": "Bad Request",
  "mensagem": "R1: o aluno não pertence à turma desta atividade",
  "caminho": "/entregas",
  "timestamp": "2026-10-08T19:30:00",
  "campos": []
}
```

Um campo inválido também devolve `400`, com a lista `campos` dizendo qual campo corrigir. Um id que não existe devolve `404`.

### As planejadas

Estão no contrato, mas ainda não respondem.

| Recurso | O que vai fazer |
|---|---|
| `/turmas` | Atualizar e remover turmas (`PUT` e `DELETE`) |
| `/alunos` | Listar, buscar, atualizar e remover alunos |
| `/atividades` | Listar, buscar, atualizar e remover atividades |
| `/entregas` | Listar as entregas |

O contrato completo, com todas as rotas e os DTOs, está em [docs/contrato-da-api.md](docs/contrato-da-api.md).

## Como executar

Pré-requisitos: [uv](https://docs.astral.sh/uv/), Docker Desktop aberto e Git. O uv baixa o Python e as dependências sozinho.

```bash
git clone https://github.com/thiagodallo/entrega-certa.git
cd entrega-certa

docker compose up -d                                # sobe o PostgreSQL na porta 5437
uv run python -m uvicorn api.main:app --port 8000   # aplica as migrations e sobe a API
```

Com a API no ar:

| Endereço | O que é |
|---|---|
| <http://localhost:8000/swagger-ui.html> | Swagger UI: as rotas, com **Try it out** para enviar requisições |
| <http://localhost:8000/v3/api-docs> | O contrato OpenAPI em JSON |

Para testar as rotas, use o Swagger UI ou o **Postman**. No Postman, importe todas as rotas de uma vez: **Import** → **Link** → `http://localhost:8000/v3/api-docs`.

Para parar: `Ctrl+C` na API e `docker compose stop` no banco. Para apagar o banco e rodar as migrations do zero: `docker compose down -v` e suba de novo.

## Situação do projeto

| Parte | Situação |
|---|---|
| Desenho | Em andamento: problema e regras neste README; primeira versão do modelo e do contrato em `docs/` |
| Estrutura | As 4 entidades têm todas as camadas |
| API e regras | A API simples de `/turmas`, os cadastros de alunos e de atividades e o registro, o reenvio e a correção de entregas funcionam, com `400` e `404`. As quatro regras, R1 a R4, estão implementadas no `EntregaService` |

**Ainda não funciona:** `GET /entregas`, `PUT` e `DELETE` de `/turmas` e as rotas de `/alunos` e de `/atividades` além do `POST`. Ficam para a próxima etapa, porque nenhuma regra depende delas.

## Documentação

| Documento | O que tem |
|---|---|
| [Modelo de domínio](docs/modelo-de-dominio.md) | Entidades, relacionamentos, diagrama das tabelas, migrations |
| [Contrato da API](docs/contrato-da-api.md) | Todas as rotas, os DTOs, exemplos de JSON e erros |
| [Autoavaliação](docs/autoavaliacao.md) | Os critérios da revisão do código, marcados pelo grupo |

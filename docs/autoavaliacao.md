# Autoavaliação

Os 10 critérios que serão avaliados na revisão do código, descritos em `Aula 10-11/AVALIACAO.md`, no repositório da disciplina. Para cada um, a marca do grupo e onde está a evidência.

- ✅ atende
- ◐ atende em parte (diga o que falta)
- ❌ não atende

| Critério | Marca | Evidência |
|---|---|---|
| P1 A API sobe seguindo o README | ✅ | `README.md`, seção "Como executar": `docker compose up -d` e `uv run python -m uvicorn api.main:app --port 8000`. As migrations rodam na subida |
| P2 Cada classe no pacote da sua camada | ✅ | Pastas `controller`, `service`, `mapper`, `repository`, `model`, `dto` e `config` em `api/`, com os nomes da convenção (`TurmaService`, `TurmaRequestDTO`, `TurmaNaoEncontradaException`) |
| P3 Migrations e `@Entity` de todas as tabelas, e a API sobe | ✅ | `db/migration/V1__criar_turmas.py` a `V4__criar_entregas.py`, com as chaves estrangeiras; entidades `Turma`, `Aluno`, `Atividade` e `Entrega` em `api/model/`. `api/config/migracoes.py` impede a API de subir se uma entidade não bater com a tabela |
| P4 DTOs de entrada e de saída de todas as entidades | ✅ | `api/dto/`: `TurmaRequestDTO` e `TurmaResponseDTO`, `AlunoRequestDTO` e `AlunoResponseDTO`, `AtividadeRequestDTO` e `AtividadeResponseDTO`, `EntregaRequestDTO`, `EntregaReenvioRequestDTO`, `EntregaCorrecaoRequestDTO` e `EntregaResponseDTO`, com validação no Pydantic. Nenhum Controller importa `api.model` |
| P5 Repository, Mapper, Service e Controller de todas, com o comentário no topo, e o mapa da estrutura | ✅ | `api/repository/`, `api/mapper/`, `api/service/` e `api/controller/`, um arquivo por entidade, ligados pelo construtor com `Depends`. Todo arquivo de classe começa pelo cabeçalho CAMADA, RESPONSABILIDADE, REGRAS, ROTAS ATENDIDAS e SITUAÇÃO. Mapa em `README.md`, seção "Arquitetura" |
| P6 API simples: `POST`, `GET` e `GET /{id}`, com `400` e `404` | ✅ | `api/controller/turma_controller.py` e `api/service/turma_service.py`. O `404` nasce em `TurmaNaoEncontradaException`, lançada no Service; o `400` vem da validação do `TurmaRequestDTO`. Os dois saem no `ErroDTO` por `api/controller/api_exception_handler.py` |
| P7 No mínimo 3 regras de negócio implementadas, com `400` quando violadas | ✅ | Quatro regras em `api/service/entrega_service.py`, com `RegraDeNegocioException` e mensagem que começa pelo número da regra: R1, R2 e R3 em `POST /entregas`, R2 e R3 em `PUT /entregas/{id}/reenvio`, R4 em `PUT /entregas/{id}/correcao` |
| P8 As regras atendem ao problema e ao tema | ✅ | `README.md`, seção "O problema": as regras tratam do controle de entregas com prazo (tema Educação e Aprendizagem), com a mesma tolerância de atraso para todos e o bloqueio de troca depois da correção |
| P9 Código igual ao desenho | ✅ | Entidades e colunas iguais a `docs/modelo-de-dominio.md` e rotas iguais a `docs/contrato-da-api.md`, que marca na coluna Funciona as rotas que já respondem |
| P10 README completo e bem escrito | ✅ | `README.md`: integrantes, problema, regras, tecnologias, tabela "Python no lugar de Java" com cada critério, arquitetura, rotas, como executar e situação do projeto, dizendo o que funciona e o que não |

**Pontos que o grupo espera no projeto:** 5,0

A apresentação vale os outros 5,0 pontos: são 3 perguntas, feitas na Aula 11.

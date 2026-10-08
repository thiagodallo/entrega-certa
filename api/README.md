# api: o código do projeto

**Objetivo desta pasta:** ter o projeto inteiro organizado em camadas. Todas as entidades com suas tabelas e classes criadas, a API simples funcionando e as regras de negócio implementadas.

O template da disciplina é em Java + Spring Boot. Este projeto usa Python, com as mesmas camadas e os mesmos nomes de classe.

## As pastas

Uma pasta por camada. Cada uma tem um `README.md` explicando o que fazer ali.

| Pasta | O que mora ali | Um arquivo por entidade | Classe |
|---|---|---|---|
| [controller/](controller) | A porta de entrada da API | `turma_controller.py` | `router` (APIRouter) |
| [service/](service) | As regras do sistema | `turma_service.py` | `TurmaService` |
| [mapper/](mapper) | A conversão entre DTO e entidade | `turma_mapper.py` | `TurmaMapper` |
| [repository/](repository) | A conversa com o banco | `turma_repository.py` | `TurmaRepository` |
| [model/](model) | As entidades | `turma.py` | `Turma` |
| [dto/](dto) | O JSON que entra e o que sai | `turma_request_dto.py`, `turma_response_dto.py` | `TurmaRequestDTO`, `TurmaResponseDTO` |
| [config/](config) | Banco, migrations e Swagger | Não se aplica | Não se aplica |

O nome do arquivo segue o padrão do Python (`snake_case`). O nome da classe é o mesmo da convenção da disciplina.

## Passo a passo

Para **cada** entidade de `docs/modelo-de-dominio.md`, nesta ordem:

1. **Migration**, em `db/migration`: a tabela, as colunas e as chaves estrangeiras.
2. **Entidade**, em `model/`: os atributos e os relacionamentos, iguais aos da migration. Importe a classe em `model/__init__.py`.
3. **Repository**, em `repository/`: a classe que recebe a sessão do banco no construtor.
4. **DTOs**, em `dto/`: o de entrada, com as validações, e o de saída.
5. **Mapper**, **Service** e **Controller**: só a classe (ou o `router`), com as dependências no construtor e o comentário no topo. O `router` é registrado em `main.py`.

Suba a API depois de cada entidade:

```bash
uv run python -m uvicorn api.main:app --port 8000
```

Se a entidade não bater com a tabela, a API não sobe e o erro diz qual coluna está errada.

Com todas as entidades criadas:

1. Escolha a mais simples e faça as três rotas da API simples: `POST`, `GET` e `GET /{id}`.
2. Implemente as regras de negócio do README no Service, com as rotas que elas precisam. Quando uma regra é violada, o Service lança `RegraDeNegocioException` e o cliente recebe `400` com a mensagem da regra.

As classes que nenhuma rota usa ainda ficam montadas.

## Como as classes se ligam

As dependências entram pelo construtor, e quem monta os objetos é o FastAPI (`Depends`), a cada requisição:

```python
class EntregaService:
    def __init__(
        self,
        repository: Annotated[EntregaRepository, Depends()],
        mapper: Annotated[EntregaMapper, Depends()],
    ):
        self.repository = repository
        self.mapper = mapper
```

## O comentário no topo de cada arquivo

Todo arquivo de classe que o grupo cria começa com um comentário dizendo o que ela é e o que faz. É a documentação da estrutura.

```python
# CAMADA: Service
# RESPONSABILIDADE: regras de negócio das entregas.
# REGRAS: R1 (só entrega quem é da turma da atividade) e
#         R2 (atraso de até 3 dias, com teto reduzido).
# ROTAS ATENDIDAS: as de /entregas em docs/contrato-da-api.md.
# SITUAÇÃO: montada. A lógica entra quando a rota for implementada.
```

| Linha | O que escrever | Em quais classes |
|---|---|---|
| `CAMADA` | Controller, Service, Mapper, Repository, Model ou DTO | Todas |
| `RESPONSABILIDADE` | Uma frase: o que esta classe faz no projeto | Todas |
| `REGRAS` | As regras do README que ela aplica | Service |
| `ROTAS ATENDIDAS` | As rotas de `docs/contrato-da-api.md` que ela atende | Controller e Service |
| `SITUAÇÃO` | `montada` ou `implementada` | Todas |

Uma classe **montada** existe, está ligada às outras e diz o que vai fazer, mas ainda não tem lógica. Quando ganhar os métodos, a linha `SITUAÇÃO` muda para `implementada`.

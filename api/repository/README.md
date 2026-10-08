# repository: a conversa com o banco

É a única camada que lê e grava no banco. Só o Service chama o Repository.

**Nesta etapa:** crie o Repository de todas as entidades. Em Java basta estender `JpaRepository`. Em Python a classe recebe a sessão do banco no construtor e escreve as consultas com o SQLAlchemy:

```python
class TurmaRepository:
    def __init__(self, sessao: Annotated[Session, Depends(obter_sessao)]):
        self.sessao = sessao
```

Os métodos seguem os nomes do Spring Data, para o código ficar igual ao desenho da disciplina: `save`, `find_by_id`, `find_all`.

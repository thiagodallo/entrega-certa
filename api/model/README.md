# model: as entidades

Cada classe daqui representa uma tabela do banco. São as entidades de `docs/modelo-de-dominio.md`.

**Nesta etapa:** crie a entidade de todas as tabelas, completa. A API só sobe se cada entidade bater com a sua migration.

O que toda entidade tem:

- herda de `Base` (`api/model/base.py`), o equivalente ao `@Entity`;
- `__tablename__` com o nome da tabela que a migration criou;
- `id` como chave primária gerada pelo banco;
- um atributo `Mapped[...]` por coluna, com o mesmo tipo e a mesma obrigatoriedade da migration;
- `ForeignKey` e `relationship` nos relacionamentos, com a chave estrangeira na migration;
- a importação em `api/model/__init__.py`, para a conferência com o banco enxergar a classe.

A entidade nunca aparece no Controller nem no JSON: quem viaja pela API é o DTO.

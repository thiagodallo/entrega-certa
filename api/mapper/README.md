# mapper: a conversão entre DTO e entidade

O Mapper transforma o DTO que chegou em entidade, e a entidade em DTO para devolver.

**Nesta etapa:** crie um Mapper para cada entidade. Precisam ter métodos o da API simples (`to_entity`, `to_response` e `to_response_list`) e os que as rotas das regras de negócio usam.

| Método | O que converte | Usado em |
|---|---|---|
| `to_entity(request_dto)` | DTO de entrada em entidade nova | `POST` |
| `to_response(entidade)` | Entidade em DTO de saída | Toda resposta |
| `to_response_list(entidades)` | Lista de entidades em lista de DTOs | `GET` de listagem |
| `update_entity(entidade, request_dto)` | Copia os campos do DTO para uma entidade que já existe | `PUT`, nas próximas etapas |

O Mapper não consulta o banco e não tem regra de negócio. Quando a conversão precisa de outra entidade, o Service busca e entrega pronta.

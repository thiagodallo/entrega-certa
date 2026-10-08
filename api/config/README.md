# config: configuração da aplicação

Arquivos de configuração, que não pertencem a nenhuma entidade.

| Arquivo | O que faz | Equivalente no template em Java |
|---|---|---|
| `banco.py` | Conexão com o PostgreSQL e uma sessão por requisição | `application.properties` (`spring.datasource.*`) |
| `migracoes.py` | Aplica as migrations na subida e confere se as entidades batem com as tabelas | Flyway e `ddl-auto=validate` |
| `openapi_config.py` | Título e descrição do Swagger UI, em `/swagger-ui.html` e `/v3/api-docs` | `OpenApiConfig` |

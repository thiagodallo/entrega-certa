# CAMADA: DTO
# RESPONSABILIDADE: classe-mãe dos DTOs das entidades. Faz o JSON usar camelCase
#                   (turmaId) enquanto o Python usa snake_case (turma_id) e tira
#                   os espaços das pontas dos textos.
# SITUAÇÃO: implementada.
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

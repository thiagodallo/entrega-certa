# CAMADA: Service
# RESPONSABILIDADE: erro 404 de entrega. O Service lança quando o id não existe.
# SITUAÇÃO: implementada.
from api.service.recurso_nao_encontrado_exception import RecursoNaoEncontradoException


class EntregaNaoEncontradaException(RecursoNaoEncontradoException):
    def __init__(self, entrega_id: int):
        super().__init__(f"Entrega não encontrada: {entrega_id}")
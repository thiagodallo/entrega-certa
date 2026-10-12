# CAMADA: Service
# RESPONSABILIDADE: erro 404 de atividade. O Service lança quando o id não existe.
# SITUAÇÃO: implementada.
from api.service.recurso_nao_encontrado_exception import RecursoNaoEncontradoException


class AtividadeNaoEncontradaException(RecursoNaoEncontradoException):
    def __init__(self, atividade_id: int):
        super().__init__(f"Atividade não encontrada: {atividade_id}")

# CAMADA: Service
# RESPONSABILIDADE: erro 404 de turma. O Service lança quando o id não existe.
# SITUAÇÃO: implementada.
from api.service.recurso_nao_encontrado_exception import RecursoNaoEncontradoException


class TurmaNaoEncontradaException(RecursoNaoEncontradoException):
    def __init__(self, turma_id: int):
        super().__init__(f"Turma não encontrada: {turma_id}")

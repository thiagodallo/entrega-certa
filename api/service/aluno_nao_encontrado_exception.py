# CAMADA: Service
# RESPONSABILIDADE: erro 404 de aluno. O Service lança quando o id não existe.
# SITUAÇÃO: implementada.
from api.service.recurso_nao_encontrado_exception import RecursoNaoEncontradoException


class AlunoNaoEncontradoException(RecursoNaoEncontradoException):
    def __init__(self, aluno_id: int):
        super().__init__(f"Aluno não encontrado: {aluno_id}")

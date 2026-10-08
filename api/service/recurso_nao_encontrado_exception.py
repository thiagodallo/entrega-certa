# CAMADA: Service
# RESPONSABILIDADE: classe-mãe dos erros 404. Cada entidade cria a sua exceção
#                   herdando desta, e o Service lança quando o id não existe.
# SITUAÇÃO: implementada.
class RecursoNaoEncontradoException(Exception):
    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem

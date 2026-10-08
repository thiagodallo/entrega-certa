# CAMADA: Service
# RESPONSABILIDADE: erro de regra de negócio violada. O Service lança com a
#                   mensagem que explica a regra, e o cliente recebe 400.
# SITUAÇÃO: implementada.
class RegraDeNegocioException(Exception):
    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem

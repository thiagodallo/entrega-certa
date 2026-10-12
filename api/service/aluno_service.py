# CAMADA: Service
# RESPONSABILIDADE: cadastrar alunos em uma turma.
# REGRAS: nenhuma regra numerada. Garante que a turma existe (404) e que o
#         e-mail não está em uso por outro aluno (400). O aluno cadastrado aqui
#         é o que a R1 confere em EntregaService.
# ROTAS ATENDIDAS: POST /alunos.
# SITUAÇÃO: implementada em parte. GET, PUT e DELETE de /alunos entram na
#           próxima etapa.
from typing import Annotated

from fastapi import Depends

from api.dto.aluno_request_dto import AlunoRequestDTO
from api.dto.aluno_response_dto import AlunoResponseDTO
from api.mapper.aluno_mapper import AlunoMapper
from api.repository.aluno_repository import AlunoRepository
from api.repository.turma_repository import TurmaRepository
from api.service.regra_de_negocio_exception import RegraDeNegocioException
from api.service.turma_nao_encontrada_exception import TurmaNaoEncontradaException


class AlunoService:
    def __init__(
        self,
        repository: Annotated[AlunoRepository, Depends()],
        turma_repository: Annotated[TurmaRepository, Depends()],
        mapper: Annotated[AlunoMapper, Depends()],
    ):
        self.repository = repository
        self.turma_repository = turma_repository
        self.mapper = mapper

    def criar(self, request: AlunoRequestDTO) -> AlunoResponseDTO:
        turma = self.turma_repository.find_by_id(request.turma_id)
        if turma is None:
            raise TurmaNaoEncontradaException(request.turma_id)
        if self.repository.exists_by_email(request.email):
            raise RegraDeNegocioException("Já existe um aluno com este e-mail")
        aluno = self.repository.save(self.mapper.to_entity(request, turma))
        return self.mapper.to_response(aluno)

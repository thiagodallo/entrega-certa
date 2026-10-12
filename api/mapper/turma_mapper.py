# CAMADA: Mapper
# RESPONSABILIDADE: converter TurmaRequestDTO em Turma e Turma em TurmaResponseDTO.
# ROTAS ATENDIDAS: as de /turmas em docs/contrato-da-api.md.
# SITUAÇÃO: implementada.
from api.dto.turma_request_dto import TurmaRequestDTO
from api.dto.turma_response_dto import TurmaResponseDTO
from api.model.turma import Turma


class TurmaMapper:
    def to_entity(self, request: TurmaRequestDTO) -> Turma:
        return Turma(nome=request.nome, disciplina=request.disciplina)

    def to_response(self, turma: Turma) -> TurmaResponseDTO:
        return TurmaResponseDTO(id=turma.id, nome=turma.nome, disciplina=turma.disciplina)

    def to_response_list(self, turmas: list[Turma]) -> list[TurmaResponseDTO]:
        return [self.to_response(turma) for turma in turmas]

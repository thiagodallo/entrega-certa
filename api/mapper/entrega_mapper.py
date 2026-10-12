# CAMADA: Mapper
# RESPONSABILIDADE: converter EntregaRequestDTO em Entrega e Entrega em
#                   EntregaResponseDTO. A atividade e o aluno chegam prontos do
#                   Service, que também preenche data, atraso e teto da nota.
# ROTAS ATENDIDAS: as de /entregas em docs/contrato-da-api.md.
# SITUAÇÃO: implementada.
from decimal import Decimal

from api.dto.aluno_resumo_response_dto import AlunoResumoResponseDTO
from api.dto.atividade_resumo_response_dto import AtividadeResumoResponseDTO
from api.dto.entrega_request_dto import EntregaRequestDTO
from api.dto.entrega_response_dto import EntregaResponseDTO
from api.model.aluno import Aluno
from api.model.atividade import Atividade
from api.model.entrega import Entrega


class EntregaMapper:
    def to_entity(self, request: EntregaRequestDTO, atividade: Atividade, aluno: Aluno) -> Entrega:
        return Entrega(atividade=atividade, aluno=aluno, link=request.link)

    def to_response(self, entrega: Entrega) -> EntregaResponseDTO:
        return EntregaResponseDTO(
            id=entrega.id,
            atividade=self._resumir_atividade(entrega.atividade),
            aluno=AlunoResumoResponseDTO(id=entrega.aluno.id, nome=entrega.aluno.nome),
            link=entrega.link,
            entregue_em=entrega.entregue_em,
            atrasada=entrega.atrasada,
            nota_teto=float(entrega.nota_teto),
            nota=self._converter_nota(entrega.nota),
            corrigida_em=entrega.corrigida_em,
        )

    def to_response_list(self, entregas: list[Entrega]) -> list[EntregaResponseDTO]:
        return [self.to_response(entrega) for entrega in entregas]

    def _resumir_atividade(self, atividade: Atividade) -> AtividadeResumoResponseDTO:
        return AtividadeResumoResponseDTO(
            id=atividade.id,
            titulo=atividade.titulo,
            prazo=atividade.prazo,
            nota_maxima=float(atividade.nota_maxima),
        )

    def _converter_nota(self, nota: Decimal | None) -> float | None:
        if nota is None:
            return None
        return float(nota)

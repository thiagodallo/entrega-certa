# CAMADA: Service
# RESPONSABILIDADE: regras de negócio das entregas.
# REGRAS: R1 (só entrega o aluno que pertence à turma da atividade),
#         R2 (até 1 dia depois do prazo a entrega é aceita com teto de 70% da
#         nota máxima; depois disso é recusada) e
#         R3 (uma entrega por aluno em cada atividade; pode reenviar enquanto
#         não for corrigida, depois não) e
#         R4 (a nota da correção não passa do teto da entrega).
# ROTAS ATENDIDAS: POST /entregas, GET /entregas, GET /entregas/{id},
#                  PUT /entregas/{id}/reenvio e PUT /entregas/{id}/correcao.
# SITUAÇÃO: implementada.
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated

from fastapi import Depends

from api.dto.entrega_correcao_request_dto import EntregaCorrecaoRequestDTO
from api.dto.entrega_reenvio_request_dto import EntregaReenvioRequestDTO
from api.dto.entrega_request_dto import EntregaRequestDTO
from api.dto.entrega_response_dto import EntregaResponseDTO
from api.mapper.entrega_mapper import EntregaMapper
from api.model.entrega import Entrega
from api.repository.aluno_repository import AlunoRepository
from api.repository.atividade_repository import AtividadeRepository
from api.repository.entrega_repository import EntregaRepository
from api.service.aluno_nao_encontrado_exception import AlunoNaoEncontradoException
from api.service.atividade_nao_encontrada_exception import AtividadeNaoEncontradaException
from api.service.entrega_nao_encontrada_exception import EntregaNaoEncontradaException
from api.service.regra_de_negocio_exception import RegraDeNegocioException

TOLERANCIA_DE_ATRASO = timedelta(days=1)
FATOR_DO_TETO_COM_ATRASO = Decimal("0.70")
CENTAVOS = Decimal("0.01")


class EntregaService:
    def __init__(
        self,
        repository: Annotated[EntregaRepository, Depends()],
        atividade_repository: Annotated[AtividadeRepository, Depends()],
        aluno_repository: Annotated[AlunoRepository, Depends()],
        mapper: Annotated[EntregaMapper, Depends()],
    ):
        self.repository = repository
        self.atividade_repository = atividade_repository
        self.aluno_repository = aluno_repository
        self.mapper = mapper

    def registrar(self, request: EntregaRequestDTO) -> EntregaResponseDTO:
        atividade = self.atividade_repository.find_by_id(request.atividade_id)
        if atividade is None:
            raise AtividadeNaoEncontradaException(request.atividade_id)
        aluno = self.aluno_repository.find_by_id(request.aluno_id)
        if aluno is None:
            raise AlunoNaoEncontradoException(request.aluno_id)
        if aluno.turma_id != atividade.turma_id:
            raise RegraDeNegocioException("R1: o aluno não pertence à turma desta atividade")
        if self.repository.exists_by_atividade_id_and_aluno_id(atividade.id, aluno.id):
            raise RegraDeNegocioException("R3: o aluno já tem uma entrega para esta atividade")
        entrega = self.mapper.to_entity(request, atividade, aluno)
        self._aplicar_prazo(entrega, datetime.now().replace(microsecond=0))
        return self.mapper.to_response(self.repository.save(entrega))

    def listar(self) -> list[EntregaResponseDTO]:
        return self.mapper.to_response_list(self.repository.find_all())

    def buscar_por_id(self, entrega_id: int) -> EntregaResponseDTO:
        return self.mapper.to_response(self._buscar_entrega(entrega_id))

    def reenviar(self, entrega_id: int, request: EntregaReenvioRequestDTO) -> EntregaResponseDTO:
        entrega = self._buscar_entrega(entrega_id)
        if entrega.corrigida_em is not None:
            raise RegraDeNegocioException(
                "R3: a entrega já foi corrigida e não pode ser reenviada"
            )
        self._aplicar_prazo(entrega, datetime.now().replace(microsecond=0))
        entrega.link = request.link
        return self.mapper.to_response(self.repository.save(entrega))

    def corrigir(self, entrega_id: int, request: EntregaCorrecaoRequestDTO) -> EntregaResponseDTO:
        entrega = self._buscar_entrega(entrega_id)
        if request.nota > entrega.nota_teto:
            raise RegraDeNegocioException("R4: a nota não pode passar do teto desta entrega")
        entrega.nota = request.nota
        entrega.corrigida_em = datetime.now().replace(microsecond=0)
        return self.mapper.to_response(self.repository.save(entrega))

    def _buscar_entrega(self, entrega_id: int) -> Entrega:
        entrega = self.repository.find_by_id(entrega_id)
        if entrega is None:
            raise EntregaNaoEncontradaException(entrega_id)
        return entrega

    def _aplicar_prazo(self, entrega: Entrega, momento: datetime) -> None:
        atividade = entrega.atividade
        if momento.date() > atividade.prazo + TOLERANCIA_DE_ATRASO:
            raise RegraDeNegocioException("R2: o prazo de entrega com atraso (1 dia) já terminou")
        entrega.entregue_em = momento
        entrega.atrasada = momento.date() > atividade.prazo
        entrega.nota_teto = self._calcular_teto(atividade.nota_maxima, entrega.atrasada)

    def _calcular_teto(self, nota_maxima: Decimal, atrasada: bool) -> Decimal:
        if not atrasada:
            return nota_maxima
        return (nota_maxima * FATOR_DO_TETO_COM_ATRASO).quantize(CENTAVOS, ROUND_HALF_UP)

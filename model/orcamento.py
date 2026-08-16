# model/orcamento.py — ESQUELETO (RED)
class Orcamento:
    def __init__(self, cliente, imovel):
        self._cliente = cliente
        self._imovel = imovel
        self._valor_mensal = 0.0
        self._contrato = None
        self._parcelas = []

    @property
    def cliente(self): return self._cliente
    @property
    def imovel(self): return self._imovel
    @property
    def valor_mensal(self): return self._valor_mensal
    @property
    def contrato(self): return self._contrato
    @property
    def parcelas(self): return self._parcelas

    def gerar_orcamento(self):
        self._valor_mensal = self._imovel.calcular_mensalidade(self._cliente)
        return self

    def gerar_parcelas_csv(self, total_meses=12) -> list:
        # TODO: RED — deve retornar 12 parcelas mensais (RF-09)
        return []
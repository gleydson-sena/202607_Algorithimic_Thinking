from .contrato import Contrato

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
        self._contrato = Contrato()
        self._parcelas = self._contrato.calcular_parcelas()
        return self

    def gerar_parcelas_csv(self, total_meses=12) -> list:
        return [{"mes": i, "valor": self._valor_mensal} for i in range(1, total_meses + 1)]
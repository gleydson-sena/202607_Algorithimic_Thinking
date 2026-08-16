class Contrato:
    def __init__(self, valor_total=2000.0, max_parcelas=5):
        self._valor_total = valor_total
        self._max_parcelas = max_parcelas

    @property
    def valor_total(self): return self._valor_total
    @property
    def max_parcelas(self): return self._max_parcelas

    def calcular_parcelas(self) -> list:
        valor = round(self._valor_total / self._max_parcelas, 2)
        return [{"numero": i, "valor": valor} for i in range(1, self._max_parcelas + 1)]
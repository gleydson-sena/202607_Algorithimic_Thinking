# model/contrato.py — ESQUELETO (RED)
class Contrato:
    def __init__(self, valor_total=2000.0, max_parcelas=5):
        self._valor_total = valor_total
        self._max_parcelas = max_parcelas

    @property
    def valor_total(self): return self._valor_total
    @property
    def max_parcelas(self): return self._max_parcelas

    def calcular_parcelas(self) -> list:
        # TODO: RED — deve retornar 5 parcelas de 400.0 (RF-07)
        return []
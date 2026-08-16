# model/imovel.py — ESQUELETO (RED)
from abc import ABC, abstractmethod

class Imovel(ABC):
    """Classe abstrata — padrão Valor Base + Acréscimos - Desconto."""

    def __init__(self, tipo, quartos=1, tem_garagem=False, valor_base=0.0, vagas=0):
        self._tipo = tipo
        self._quartos = quartos
        self._tem_garagem = tem_garagem
        self._valor_base = valor_base
        self._vagas = vagas

    @property
    def tipo(self): return self._tipo
    @property
    def quartos(self): return self._quartos
    @property
    def tem_garagem(self): return self._tem_garagem
    @property
    def valor_base(self): return self._valor_base
    @property
    def vagas(self): return self._vagas

    @abstractmethod
    def calcular_mensalidade(self, cliente) -> float:
        """Polimorfismo: cada subclasse implementa sua regra."""
        ...

class Apartamento(Imovel):
    def __init__(self, quartos=1, tem_garagem=False):
        super().__init__("apartamento", quartos, tem_garagem, 0.0)

    def calcular_mensalidade(self, cliente) -> float:
        # TODO: RED — base 700 + 2º quarto 200 + garagem 300 - 5% sem crianças
        return 0.0

class Casa(Imovel):
    def __init__(self, quartos=1, tem_garagem=False):
        super().__init__("casa", quartos, tem_garagem, 0.0)

    def calcular_mensalidade(self, cliente) -> float:
        # TODO: RED — base 900 + 2º quarto 250 + garagem 300
        return 0.0

class Estudio(Imovel):
    def __init__(self, vagas=2):
        super().__init__("estudio", 1, False, 0.0, vagas)

    def calcular_mensalidade(self, cliente) -> float:
        # TODO: RED — base 1.200 + 2 vagas 250 + extra 60
        return 0.0
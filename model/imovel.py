from abc import ABC, abstractmethod

class Imovel(ABC):
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
        ...

class Apartamento(Imovel):
    def __init__(self, quartos=1, tem_garagem=False):
        super().__init__("apartamento", quartos, tem_garagem, 700.0)

    def calcular_mensalidade(self, cliente) -> float:
        valor = self._valor_base
        if self._quartos >= 2:
            valor += 200.0
        if self._tem_garagem:
            valor += 300.0
        if not cliente.tem_criancas:
            valor *= 0.95
        return round(valor, 2)

class Casa(Imovel):
    def __init__(self, quartos=1, tem_garagem=False):
        super().__init__("casa", quartos, tem_garagem, 900.0)

    def calcular_mensalidade(self, cliente) -> float:
        valor = self._valor_base
        if self._quartos >= 2:
            valor += 250.0
        if self._tem_garagem:
            valor += 300.0
        return round(valor, 2)

class Estudio(Imovel):
    def __init__(self, vagas=2):
        super().__init__("estudio", quartos=1, tem_garagem=False, valor_base=1200.0, vagas=vagas)

    def calcular_mensalidade(self, cliente) -> float:
        valor = self._valor_base
        if self._vagas >= 2:
            valor += 250.0
        if self._vagas > 2:
            valor += (self._vagas - 2) * 60.0
        return round(valor, 2)
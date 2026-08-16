# service/orcamento_service.py — ESQUELETO (RED)
from model.imovel import Apartamento, Casa, Estudio
from model.cliente import Cliente
from model.orcamento import Orcamento

class OrcamentoService:
    _TIPOS = {"apartamento": Apartamento, "casa": Casa, "estudio": Estudio}

    def criar_imovel(self, tipo, quartos=1, tem_garagem=False, vagas=0):
        cls = self._TIPOS[tipo]
        if tipo == "estudio":
            return cls(vagas=vagas)
        return cls(quartos=quartos, tem_garagem=tem_garagem)

    def gerar_orcamento(self, dados):
        # TODO: completar após GREEN das regras de domínio
        cliente = Cliente(dados.get("nome", ""), dados.get("email", ""),
                          dados.get("tem_criancas", False))
        imovel = self.criar_imovel(dados["tipo"], dados.get("quartos", 1),
                                   dados.get("tem_garagem", False), dados.get("vagas", 0))
        return Orcamento(cliente, imovel).gerar_orcamento()
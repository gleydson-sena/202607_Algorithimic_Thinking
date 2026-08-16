from datetime import date

from model.imovel import Apartamento, Casa, Estudio
from model.cliente import Cliente
from model.orcamento import Orcamento
import data.database as db

class OrcamentoService:
    _TIPOS = {"apartamento": Apartamento, "casa": Casa, "estudio": Estudio}

    def criar_imovel(self, tipo, quartos=1, tem_garagem=False, vagas=0):
        cls = self._TIPOS[tipo]
        if tipo == "estudio":
            return cls(vagas=vagas)
        return cls(quartos=quartos, tem_garagem=tem_garagem)

    @staticmethod
    def _vencimento(offset_meses):
        hoje = date.today()
        mes = hoje.month - 1 + offset_meses
        ano = hoje.year + mes // 12
        return f"{ano:04d}-{mes % 12 + 1:02d}-01"

    def gerar_orcamento(self, dados):
        cliente = Cliente(dados.get("nome", ""), dados.get("email", ""),
                          dados.get("tem_criancas", False))
        imovel = self.criar_imovel(dados["tipo"], dados.get("quartos", 1),
                                   dados.get("tem_garagem", False), dados.get("vagas", 0))
        orcamento = Orcamento(cliente, imovel).gerar_orcamento()

        id_cliente = db.salvar_cliente(cliente.nome, cliente.email, cliente.tem_criancas)
        id_imovel = db.salvar_imovel(imovel.tipo, imovel.quartos, imovel.tem_garagem,
                                     imovel.valor_base, imovel.vagas)
        id_orcamento = db.salvar_orcamento(id_cliente, id_imovel, orcamento.valor_mensal)
        id_contrato = db.salvar_contrato(id_orcamento,
                                         orcamento.contrato.valor_total,
                                         orcamento.contrato.max_parcelas)
        for i, p in enumerate(orcamento.gerar_parcelas_csv(), start=1):
            db.salvar_parcela(id_contrato, i, p["valor"], self._vencimento(i))

        return orcamento
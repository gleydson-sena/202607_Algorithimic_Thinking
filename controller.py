# controller.py — ESQUELETO (RED)
from service.orcamento_service import OrcamentoService

class OrcamentoController:
    def __init__(self):
        self._service = OrcamentoService()

    def validar(self, dados) -> list:
        # TODO: RED — deve retornar lista de erros (RF-12)
        return []

    def gerar_orcamento(self, dados):
        erros = self.validar(dados)
        if erros:
            raise ValueError("; ".join(erros))
        return self._service.gerar_orcamento(dados)
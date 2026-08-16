from service.orcamento_service import OrcamentoService

TIPOS_VALIDOS = ("apartamento", "casa", "estudio")

class OrcamentoController:
    def __init__(self):
        self._service = OrcamentoService()

    def validar(self, dados) -> list:
        erros = []
        if not dados.get("nome") or not str(dados["nome"]).strip():
            erros.append("Informe o nome do cliente.")
        if not dados.get("email") or "@" not in str(dados["email"]):
            erros.append("Informe um e-mail válido.")
        if dados.get("tipo") not in TIPOS_VALIDOS:
            erros.append("Selecione um tipo de imóvel válido.")
        if dados.get("tipo") == "estudio" and int(dados.get("vagas", 0) or 0) < 2:
            erros.append("Estúdio exige no mínimo 2 vagas.")
        return erros

    def gerar_orcamento(self, dados):
        erros = self.validar(dados)
        if erros:
            raise ValueError("; ".join(erros))
        return self._service.gerar_orcamento(dados)
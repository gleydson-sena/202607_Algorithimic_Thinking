import pytest

from model.cliente import Cliente
from model.imovel import Apartamento, Casa, Estudio
from model.contrato import Contrato
from model.orcamento import Orcamento
from controller import OrcamentoController

def test_apartamento_1_quarto_sem_opcionais_com_criancas():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=True)
    assert Apartamento().calcular_mensalidade(cliente) == 700.0

def test_casa_1_quarto_sem_opcionais():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=True)
    assert Casa().calcular_mensalidade(cliente) == 900.0

def test_estudio_2_vagas():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=True)
    assert Estudio(vagas=2).calcular_mensalidade(cliente) == 1450.0

def test_apartamento_2_quartos_acrescimo_200():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=True)
    assert Apartamento(quartos=2).calcular_mensalidade(cliente) == 900.0

def test_casa_2_quartos_acrescimo_250():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=True)
    assert Casa(quartos=2).calcular_mensalidade(cliente) == 1150.0

def test_apartamento_com_garagem_acrescimo_300():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=True)
    assert Apartamento(tem_garagem=True).calcular_mensalidade(cliente) == 1000.0

def test_casa_2_quartos_com_garagem():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=True)
    assert Casa(quartos=2, tem_garagem=True).calcular_mensalidade(cliente) == 1450.0

def test_estudio_3_vagas_vaga_extra_60():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=True)
    assert Estudio(vagas=3).calcular_mensalidade(cliente) == 1510.0

def test_estudio_4_vagas():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=True)
    assert Estudio(vagas=4).calcular_mensalidade(cliente) == 1570.0

def test_apartamento_desconto_5_porcento_sem_criancas():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=False)
    assert Apartamento().calcular_mensalidade(cliente) == 665.0

def test_apartamento_2_quartos_garagem_desconto():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=False)
    assert Apartamento(quartos=2, tem_garagem=True).calcular_mensalidade(cliente) == 1140.0

def test_casa_nao_tem_desconto_sem_criancas():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=False)
    assert Casa().calcular_mensalidade(cliente) == 900.0

def test_contrato_5_parcelas_de_400():
    contrato = Contrato()
    parcelas = contrato.calcular_parcelas()
    assert len(parcelas) == 5
    assert all(p["valor"] == 400.0 for p in parcelas)

def test_orcamento_gera_12_parcelas_csv():
    cliente = Cliente("Ana", "ana@x.com", tem_criancas=False)
    orcamento = Orcamento(cliente, Apartamento(quartos=2, tem_garagem=True)).gerar_orcamento()
    parcelas = orcamento.gerar_parcelas_csv()
    assert len(parcelas) == 12
    assert all(p["valor"] == orcamento.valor_mensal for p in parcelas)

def test_validacao_rejeita_sem_nome():
    controller = OrcamentoController()
    with pytest.raises(ValueError):
        controller.gerar_orcamento({"nome": "", "email": "a@x.com", "tipo": "casa"})

def test_validacao_rejeita_email_invalido():
    controller = OrcamentoController()
    with pytest.raises(ValueError):
        controller.gerar_orcamento({"nome": "Ana", "email": "sem-arroba", "tipo": "casa"})

def test_validacao_rejeita_estudio_com_menos_de_2_vagas():
    controller = OrcamentoController()
    with pytest.raises(ValueError):
        controller.gerar_orcamento({"nome": "Ana", "email": "a@x.com", "tipo": "estudio", "vagas": 1})
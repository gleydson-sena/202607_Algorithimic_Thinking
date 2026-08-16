# app.py — View (Streamlit). Rode com: streamlit run app.py
import csv
import io

import streamlit as st

from controller import OrcamentoController

st.set_page_config(page_title="Orçamento de Aluguel — Imobiliária R.M.", page_icon="🏠")
st.title("🏠 Orçamento de Aluguel — Imobiliária R.M.")
st.caption("Algorithmic Thinking & Introduction to Object-Oriented Programming")

controller = OrcamentoController()

# ---------- Dados do Cliente ----------
st.subheader("Dados do Cliente")
nome = st.text_input("Nome completo *")
email = st.text_input("E-mail (opcional)")
tem_criancas = st.checkbox("Possui crianças?")

# ---------- Imóvel ----------
st.subheader("Imóvel")
tipo = st.selectbox("Tipo de imóvel *", ["apartamento", "casa", "estudio"])

quartos, tem_garagem, vagas = 1, False, 0
if tipo in ("apartamento", "casa"):
    quartos = st.number_input("Quantidade de quartos", 1, 4, 1)
    tem_garagem = st.checkbox("Vaga de garagem")
else:
    vagas = st.number_input("Vagas de estacionamento", 2, 10, 2)

# ---------- Gerar ----------
if st.button("Gerar Orçamento"):
    dados = {"nome": nome, "email": email, "tem_criancas": tem_criancas,
             "tipo": tipo, "quartos": quartos, "tem_garagem": tem_garagem, "vagas": vagas}
    try:
        orcamento = controller.gerar_orcamento(dados)
        st.success("Orçamento gerado e persistido no SQLite!")

        st.metric("Valor mensal do aluguel", f"R$ {orcamento.valor_mensal:,.2f}")

        # Parcela do contrato: R$ 400,00 nos meses 1 a 5; R$ 0,00 nos meses 6 a 12
        parcela_contrato = orcamento.parcelas[0]["valor"] if orcamento.parcelas else 0.0
        linhas = []
        for mes in range(1, 13):
            vlr_aluguel = orcamento.valor_mensal
            vlr_contrato = parcela_contrato if mes <= 5 else 0.00
            linhas.append({
                "mes": mes,
                "vlr_aluguel": round(vlr_aluguel, 2),
                "vlr_contrato": round(vlr_contrato, 2),
                "total": round(vlr_aluguel + vlr_contrato, 2),
            })

        st.subheader("Cronograma de 12 meses (vlr_aluguel + vlr_contrato = total)")
        st.dataframe(linhas, use_container_width=True)

        # CSV com as mesmas colunas
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["mes", "vlr_aluguel", "vlr_contrato", "total"])
        for l in linhas:
            writer.writerow([l["mes"], f"{l['vlr_aluguel']:.2f}",
                             f"{l['vlr_contrato']:.2f}", f"{l['total']:.2f}"])
        st.download_button("📥 Baixar CSV (12 meses)", buf.getvalue(),
                           "orcamento_12_parcelas.csv", "text/csv")
    except ValueError as e:
        st.error(str(e))
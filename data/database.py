import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "orcamento.db"

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def salvar_cliente(nome, email, tem_criancas):
    with conectar() as conn:
        cur = conn.execute(
            "INSERT INTO cliente (nome, email, tem_criancas) VALUES (?, ?, ?)",
            (nome, email, int(tem_criancas)))
        return cur.lastrowid

def salvar_imovel(tipo, quartos, tem_garagem, valor_base, vagas):
    with conectar() as conn:
        cur = conn.execute(
            "INSERT INTO imovel (tipo, quartos, tem_garagem, valor_base, vagas) "
            "VALUES (?, ?, ?, ?, ?)",
            (tipo, quartos, int(tem_garagem), valor_base, vagas))
        return cur.lastrowid

def salvar_orcamento(id_cliente, id_imovel, valor_mensal):
    with conectar() as conn:
        cur = conn.execute(
            "INSERT INTO orcamento (id_cliente, id_imovel, valor_mensal) VALUES (?, ?, ?)",
            (id_cliente, id_imovel, valor_mensal))
        return cur.lastrowid

def salvar_contrato(id_orcamento, valor_total=2000.0, max_parcelas=5):
    with conectar() as conn:
        cur = conn.execute(
            "INSERT INTO contrato (id_orcamento, valor_total, max_parcelas) VALUES (?, ?, ?)",
            (id_orcamento, valor_total, max_parcelas))
        return cur.lastrowid

def salvar_parcela(id_contrato, numero, valor, vencimento):
    with conectar() as conn:
        conn.execute(
            "INSERT INTO parcela (id_contrato, numero, valor, vencimento) VALUES (?, ?, ?, ?)",
            (id_contrato, numero, valor, vencimento))
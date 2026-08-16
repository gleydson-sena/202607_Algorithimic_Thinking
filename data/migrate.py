# data/migrate.py
"""Migração 001 — Criação do banco SQLite (modelo físico do modelo ER).

Executar com: python data/migrate.py
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "orcamento.db"

DDL = """
-- ============================================================
-- MODELO FÍSICO DE DADOS — Imobiliária R.M.
-- Base: modelo Entidade-Relacionamento (5 entidades)
-- ============================================================

-- ============================================================
-- RELACIONAMENTOS (cardinalidades do modelo ER)
--   1) cliente  1 --- N  orcamento   (um cliente gera vários orçamentos)
--   2) imovel   1 --- N  orcamento   (um imóvel é orçado várias vezes)
--   3) orcamento 1 --- 1 contrato    (um orçamento origina um contrato)
--   4) contrato 1 --- N  parcela     (um contrato possui 12 parcelas)
-- Implementados via FOREIGN KEY nos blocos abaixo.
-- ============================================================

-- 1) CLIENTE (RF-10; RF-06: tem_criancas = gatilho do desconto 5%)
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          VARCHAR(100) NOT NULL,
    email         VARCHAR(100) NOT NULL,
    tem_criancas  INTEGER NOT NULL DEFAULT 0 CHECK (tem_criancas IN (0, 1))
);

-- 2) IMOVEL (RF-01 a RF-05) — herança via discriminador tipo (single table)
CREATE TABLE IF NOT EXISTS imovel (
    id_imovel    INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo         VARCHAR(20) NOT NULL CHECK (tipo IN ('apartamento', 'casa', 'estudio')),
    quartos      INTEGER NOT NULL DEFAULT 1,
    tem_garagem  INTEGER NOT NULL DEFAULT 0 CHECK (tem_garagem IN (0, 1)),
    valor_base   DECIMAL(10, 2) NOT NULL,
    vagas        INTEGER NOT NULL DEFAULT 0
);

-- 3) ORCAMENTO (RF-08) — RELACIONA cliente 1-N e imovel 1-N
CREATE TABLE IF NOT EXISTS orcamento (
    id_orcamento  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente    INTEGER NOT NULL,
    id_imovel     INTEGER NOT NULL,
    valor_mensal  DECIMAL(10, 2) NOT NULL,
    data_emissao  TEXT NOT NULL DEFAULT (date('now')),
    FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente),
    FOREIGN KEY (id_imovel)  REFERENCES imovel  (id_imovel)
);

-- 4) CONTRATO (RF-07) — RELACIONA orcamento 1-1 (valor R$ 2.000, até 5x)
CREATE TABLE IF NOT EXISTS contrato (
    id_contrato   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_orcamento  INTEGER NOT NULL UNIQUE,
    valor_total   DECIMAL(10, 2) NOT NULL DEFAULT 2000.00,
    max_parcelas  INTEGER NOT NULL DEFAULT 5,
    FOREIGN KEY (id_orcamento) REFERENCES orcamento (id_orcamento)
);

-- 5) PARCELA (RF-09) — RELACIONA contrato 1-N (12 parcelas do CSV)
CREATE TABLE IF NOT EXISTS parcela (
    id_parcela   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_contrato  INTEGER NOT NULL,
    numero       INTEGER NOT NULL,
    valor        DECIMAL(10, 2) NOT NULL,
    vencimento   TEXT NOT NULL,
    FOREIGN KEY (id_contrato) REFERENCES contrato (id_contrato),
    UNIQUE (id_contrato, numero)
);

-- Índices para acelerar as consultas por FK
CREATE INDEX IF NOT EXISTS idx_orcamento_cliente ON orcamento (id_cliente);
CREATE INDEX IF NOT EXISTS idx_orcamento_imovel  ON orcamento (id_imovel);
CREATE INDEX IF NOT EXISTS idx_parcela_contrato  ON parcela  (id_contrato);
"""

def main():
    conn = sqlite3.connect(DB_PATH)
    # ATIVA a aplicação das FOREIGN KEY (SQLite não aplica por padrão)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(DDL)
    conn.commit()

    tabelas = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )]
    conn.close()
    print(f"Banco criado: {DB_PATH}")
    print("Tabelas:", ", ".join(tabelas))
    print("Relacionamentos (FKs) aplicados via PRAGMA foreign_keys = ON")

if __name__ == "__main__":
    main()
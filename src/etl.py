"""Extracao, validacao e transformacao da base de vendas."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "pedido_id",
    "data_pedido",
    "cliente_id",
    "regiao",
    "canal",
    "categoria",
    "produto",
    "quantidade",
    "preco_unitario",
    "desconto_pct",
    "custo_unitario",
}


def transform_sales(source: str | Path) -> pd.DataFrame:
    """Carrega vendas, valida o schema e calcula metricas financeiras."""
    df = pd.read_csv(source)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Colunas obrigatorias ausentes: {sorted(missing)}")

    df["data_pedido"] = pd.to_datetime(df["data_pedido"], errors="raise")
    numeric = ["quantidade", "preco_unitario", "desconto_pct", "custo_unitario"]
    df[numeric] = df[numeric].apply(pd.to_numeric, errors="raise")

    if df["pedido_id"].duplicated().any():
        raise ValueError("A base possui pedidos duplicados")
    if (df["quantidade"] <= 0).any() or (df["preco_unitario"] <= 0).any():
        raise ValueError("Quantidade e preco precisam ser positivos")
    if not df["desconto_pct"].between(0, 1).all():
        raise ValueError("Desconto deve estar entre 0 e 1")

    df["receita_bruta"] = df["quantidade"] * df["preco_unitario"]
    df["receita_liquida"] = df["receita_bruta"] * (1 - df["desconto_pct"])
    df["custo_total"] = df["quantidade"] * df["custo_unitario"]
    df["lucro"] = df["receita_liquida"] - df["custo_total"]
    df["margem_pct"] = (df["lucro"] / df["receita_liquida"]).mul(100)
    df["mes"] = df["data_pedido"].dt.to_period("M").astype(str)
    return df.sort_values(["data_pedido", "pedido_id"]).reset_index(drop=True)


def export_powerbi(df: pd.DataFrame, destination: str | Path) -> None:
    """Exporta uma tabela pronta para modelagem no Power BI."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False, date_format="%Y-%m-%d")


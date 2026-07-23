"""Executa a analise exploratoria e gera entregaveis do projeto."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from etl import export_powerbi, transform_sales


ROOT = Path(__file__).resolve().parents[1]


def currency(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def build_outputs() -> dict[str, float | int | str]:
    df = transform_sales(ROOT / "data" / "raw" / "vendas.csv")
    output = ROOT / "outputs"
    output.mkdir(exist_ok=True)

    export_powerbi(df, ROOT / "data" / "processed" / "vendas_powerbi.csv")
    with sqlite3.connect(output / "vendas.db") as connection:
        df.to_sql("fato_vendas", connection, if_exists="replace", index=False)

    monthly = df.groupby("mes", as_index=False).agg(
        receita=("receita_liquida", "sum"), lucro=("lucro", "sum"), pedidos=("pedido_id", "nunique")
    )
    categories = df.groupby("categoria", as_index=False).agg(
        receita=("receita_liquida", "sum"), lucro=("lucro", "sum")
    ).sort_values("receita", ascending=False)
    regions = df.groupby("regiao", as_index=False)["receita_liquida"].sum().sort_values("receita_liquida")
    monthly.to_csv(output / "vendas_por_mes.csv", index=False)
    categories.to_csv(output / "desempenho_categorias.csv", index=False)

    kpis = {
        "pedidos": int(df["pedido_id"].nunique()),
        "clientes": int(df["cliente_id"].nunique()),
        "receita_liquida": round(float(df["receita_liquida"].sum()), 2),
        "lucro": round(float(df["lucro"].sum()), 2),
        "margem_pct": round(float(100 * df["lucro"].sum() / df["receita_liquida"].sum()), 2),
        "ticket_medio": round(float(df["receita_liquida"].sum() / df["pedido_id"].nunique()), 2),
        "melhor_categoria": str(categories.iloc[0]["categoria"]),
    }
    (output / "kpis.json").write_text(json.dumps(kpis, indent=2, ensure_ascii=False), encoding="utf-8")

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle("Painel de Vendas 2025", fontsize=20, fontweight="bold")

    axes[0, 0].plot(monthly["mes"], monthly["receita"], marker="o", color="#2563eb", linewidth=2.4)
    axes[0, 0].set_title("Receita liquida por mes")
    axes[0, 0].tick_params(axis="x", rotation=45)
    axes[0, 0].set_ylabel("R$")

    axes[0, 1].bar(categories["categoria"], categories["receita"], color="#14b8a6")
    axes[0, 1].set_title("Receita por categoria")
    axes[0, 1].tick_params(axis="x", rotation=20)

    axes[1, 0].barh(regions["regiao"], regions["receita_liquida"], color="#f59e0b")
    axes[1, 0].set_title("Receita por regiao")

    axes[1, 1].axis("off")
    summary = (
        f"PEDIDOS\n{kpis['pedidos']:,}\n\n"
        f"RECEITA\n{currency(float(kpis['receita_liquida']))}\n\n"
        f"LUCRO\n{currency(float(kpis['lucro']))}\n\n"
        f"MARGEM\n{kpis['margem_pct']:.1f}%"
    )
    axes[1, 1].text(0.5, 0.52, summary, ha="center", va="center", fontsize=14, color="#0f172a")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output / "dashboard_vendas.svg", bbox_inches="tight")
    plt.close(fig)
    return kpis


if __name__ == "__main__":
    result = build_outputs()
    print(json.dumps(result, indent=2, ensure_ascii=False))

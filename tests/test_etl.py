from pathlib import Path

import pandas as pd

from src.etl import transform_sales


def test_transform_sales_calculates_financial_metrics(tmp_path: Path) -> None:
    source = tmp_path / "vendas.csv"
    pd.DataFrame(
        [{
            "pedido_id": "PED-1", "data_pedido": "2025-01-10", "cliente_id": "CLI-1",
            "regiao": "Nordeste", "canal": "Site", "categoria": "Casa", "produto": "Cafeteira",
            "quantidade": 2, "preco_unitario": 100, "desconto_pct": 0.10, "custo_unitario": 55,
        }]
    ).to_csv(source, index=False)

    result = transform_sales(source)

    assert result.loc[0, "receita_liquida"] == 180
    assert result.loc[0, "lucro"] == 70
    assert result.loc[0, "mes"] == "2025-01"


def test_transform_sales_rejects_duplicate_orders(tmp_path: Path) -> None:
    source = tmp_path / "vendas.csv"
    row = {
        "pedido_id": "PED-1", "data_pedido": "2025-01-10", "cliente_id": "CLI-1",
        "regiao": "Nordeste", "canal": "Site", "categoria": "Casa", "produto": "Cafeteira",
        "quantidade": 1, "preco_unitario": 100, "desconto_pct": 0, "custo_unitario": 55,
    }
    pd.DataFrame([row, row]).to_csv(source, index=False)

    try:
        transform_sales(source)
    except ValueError as error:
        assert "duplicados" in str(error)
    else:
        raise AssertionError("Pedidos duplicados deveriam gerar erro")


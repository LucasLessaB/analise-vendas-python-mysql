"""Gera uma base ficticia e reproduzivel de vendas de varejo."""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "data" / "raw" / "vendas.csv"

PRODUTOS = {
    "Eletronicos": [("Fone Bluetooth", 149.90, 72.00), ("Webcam HD", 229.90, 118.00), ("Teclado", 189.90, 91.00)],
    "Casa": [("Cafeteira", 249.90, 130.00), ("Luminaria", 89.90, 39.00), ("Organizador", 59.90, 22.00)],
    "Escritorio": [("Cadeira", 899.90, 510.00), ("Suporte Notebook", 119.90, 48.00), ("Mochila", 219.90, 102.00)],
    "Esporte": [("Garrafa Termica", 79.90, 29.00), ("Tapete Yoga", 109.90, 44.00), ("Kit Faixas", 69.90, 25.00)],
}
REGIOES = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
CANAIS = ["Site", "Marketplace", "Loja fisica"]


def generate_sales(rows: int = 1500, seed: int = 42) -> None:
    random.seed(seed)
    start = date(2025, 1, 1)
    records = []

    for order_id in range(1, rows + 1):
        category = random.choice(list(PRODUTOS))
        product, price, cost = random.choice(PRODUTOS[category])
        quantity = random.choices([1, 2, 3, 4, 5], weights=[47, 28, 14, 7, 4])[0]
        discount = random.choices([0, 0.05, 0.10, 0.15], weights=[55, 24, 16, 5])[0]
        order_date = start + timedelta(days=random.randint(0, 364))
        records.append(
            {
                "pedido_id": f"PED-{order_id:05d}",
                "data_pedido": order_date.isoformat(),
                "cliente_id": f"CLI-{random.randint(1, 480):04d}",
                "regiao": random.choices(REGIOES, weights=[9, 24, 10, 39, 18])[0],
                "canal": random.choices(CANAIS, weights=[45, 35, 20])[0],
                "categoria": category,
                "produto": product,
                "quantidade": quantity,
                "preco_unitario": price,
                "desconto_pct": discount,
                "custo_unitario": cost,
            }
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"Base criada: {OUTPUT} ({len(records)} linhas)")


if __name__ == "__main__":
    generate_sales()


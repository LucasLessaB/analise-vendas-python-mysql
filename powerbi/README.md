# Uso no Power BI

Importe `data/processed/vendas_powerbi.csv` e utilize:

- `receita_liquida`, `lucro` e `margem_pct` como medidas principais;
- `data_pedido` em uma tabela calendario;
- `categoria`, `regiao` e `canal` como dimensoes;
- cartões para receita, lucro, margem e ticket medio;
- grafico de linha para a evolucao mensal e barras para categorias/regioes.

O arquivo processado e recriado ao executar `python src/analysis.py`.


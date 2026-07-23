# Análise de vendas com Python e SQL

Criei este projeto para praticar um fluxo de análise do começo ao fim: receber uma base de vendas, conferir a qualidade dos dados, calcular indicadores e preparar uma tabela que possa ser usada no Power BI.

Os dados são fictícios e gerados pelo próprio projeto. Assim, qualquer pessoa consegue repetir a análise sem depender de uma base privada.

![Painel de vendas](outputs/dashboard_vendas.svg)

## O que eu quis responder

- Qual foi a receita, o lucro, a margem e o ticket médio?
- Como as vendas mudaram ao longo de 2025?
- Quais categorias e regiões tiveram o melhor resultado?
- Quais clientes concentraram o maior valor de compra?

## Resultado que obtive

Na base simulada, analisei 1.500 pedidos de 458 clientes. O resultado foi:

- receita líquida de R$ 534.960,44;
- lucro de R$ 260.826,43;
- margem de 48,76%;
- ticket médio de R$ 356,64;
- categoria Escritório com a maior receita.

Esses números servem apenas para demonstrar a análise. Não representam uma empresa real.

## Uma decisão importante

Mantive os dados brutos separados dos dados tratados. O arquivo original fica em `data/raw/`, enquanto a tabela pronta para análise fica em `data/processed/`. Isso evita alterar a fonte e facilita conferir cada transformação.

Também coloquei validações para impedir pedidos duplicados e valores inválidos de quantidade, preço ou desconto.

## Tecnologias que pratiquei

Python, Pandas, Matplotlib, SQL, MySQL, SQLite, preparação de dados para Power BI e Pytest.

## Organização do projeto

```text
data/raw/                 base fictícia original
data/processed/           tabela tratada para o Power BI
src/etl.py                validações e transformações
src/analysis.py           indicadores, tabelas, SQLite e gráfico
sql/                      estrutura MySQL e consultas de negócio
tests/                    testes do processo de ETL
outputs/                  resultados gerados
```

## Como executar

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python generate_data.py
python src/analysis.py
pytest -q
```

## Próximo passo

Quero montar o painel diretamente no Power BI e adicionar capturas das páginas do relatório. A base `data/processed/vendas_powerbi.csv` já está preparada para essa etapa.

CREATE DATABASE IF NOT EXISTS portfolio_vendas;
USE portfolio_vendas;

CREATE TABLE fato_vendas (
    pedido_id VARCHAR(12) PRIMARY KEY,
    data_pedido DATE NOT NULL,
    cliente_id VARCHAR(12) NOT NULL,
    regiao VARCHAR(20) NOT NULL,
    canal VARCHAR(20) NOT NULL,
    categoria VARCHAR(30) NOT NULL,
    produto VARCHAR(80) NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    desconto_pct DECIMAL(5, 4) NOT NULL,
    custo_unitario DECIMAL(10, 2) NOT NULL,
    receita_bruta DECIMAL(12, 2) NOT NULL,
    receita_liquida DECIMAL(12, 2) NOT NULL,
    custo_total DECIMAL(12, 2) NOT NULL,
    lucro DECIMAL(12, 2) NOT NULL,
    margem_pct DECIMAL(7, 2) NOT NULL,
    mes CHAR(7) NOT NULL
);


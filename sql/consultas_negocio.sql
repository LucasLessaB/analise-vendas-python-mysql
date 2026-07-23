-- KPIs gerais
SELECT
    COUNT(DISTINCT pedido_id) AS pedidos,
    COUNT(DISTINCT cliente_id) AS clientes,
    ROUND(SUM(receita_liquida), 2) AS receita,
    ROUND(SUM(lucro), 2) AS lucro,
    ROUND(100 * SUM(lucro) / SUM(receita_liquida), 2) AS margem_pct
FROM fato_vendas;

-- Evolucao mensal
SELECT mes, ROUND(SUM(receita_liquida), 2) AS receita, ROUND(SUM(lucro), 2) AS lucro
FROM fato_vendas
GROUP BY mes
ORDER BY mes;

-- Categorias mais rentaveis
SELECT categoria, ROUND(SUM(receita_liquida), 2) AS receita, ROUND(SUM(lucro), 2) AS lucro
FROM fato_vendas
GROUP BY categoria
ORDER BY lucro DESC;

-- Clientes com maior valor acumulado
SELECT cliente_id, COUNT(*) AS pedidos, ROUND(SUM(receita_liquida), 2) AS valor_total
FROM fato_vendas
GROUP BY cliente_id
ORDER BY valor_total DESC
LIMIT 10;


WITH gasto_por_cliente AS (
    SELECT p.cliente_id, SUM(d.cantidad * d.precio_unitario) AS gasto_total
    FROM pedidos p
    JOIN detalle_pedidos d ON d.pedido_id = p.pedido_id
    WHERE p.estado = 'completado'
    GROUP BY p.cliente_id
)
SELECT c.cliente_id, c.nombre, ROUND(g.gasto_total, 2) AS gasto_total
FROM gasto_por_cliente g
JOIN clientes c ON c.cliente_id = g.cliente_id
WHERE g.gasto_total > (SELECT AVG(gasto_total) FROM gasto_por_cliente);

SELECT DATE_TRUNC('month', p.fecha_pedido)             AS mes,
       ROUND(SUM(d.cantidad * d.precio_unitario), 2)   AS ingresos,
       COUNT(DISTINCT p.pedido_id)                     AS numero_pedidos
FROM pedidos p
JOIN detalle_pedidos d ON d.pedido_id = p.pedido_id
WHERE p.estado = 'completado'
  AND p.fecha_pedido >= DATE '2025-01-01' AND p.fecha_pedido < DATE '2026-01-01'
GROUP BY mes
ORDER BY mes;

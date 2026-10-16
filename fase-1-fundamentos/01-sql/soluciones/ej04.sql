SELECT p.pedido_id,
       c.nombre,
       p.fecha_pedido,
       ROUND(SUM(d.cantidad * d.precio_unitario), 2) AS total
FROM pedidos p
JOIN clientes c        ON c.cliente_id = p.cliente_id
JOIN detalle_pedidos d ON d.pedido_id = p.pedido_id
WHERE p.estado = 'completado'
GROUP BY p.pedido_id, c.nombre, p.fecha_pedido
ORDER BY total DESC
LIMIT 10;

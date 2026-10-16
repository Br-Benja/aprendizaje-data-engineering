SELECT cliente_id, pedido_id, fecha_pedido,
       fecha_pedido - LAG(fecha_pedido) OVER (
           PARTITION BY cliente_id ORDER BY fecha_pedido, pedido_id
       ) AS dias_desde_anterior
FROM pedidos;

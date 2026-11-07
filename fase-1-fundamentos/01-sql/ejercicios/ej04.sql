-- Ejercicio 04
-- Los 10 pedidos COMPLETADOS con mayor total. Columnas:
-- pedido_id, nombre (del cliente), fecha_pedido, total
-- total = SUM(cantidad * precio_unitario), redondeado a 2 decimales.
-- Ordena de mayor a menor total.
-- Conceptos: JOIN de 3 tablas, GROUP BY, ORDER BY + LIMIT

-- Escribe tu consulta aquí:

SELECT 
    p.pedido_id,
    c.nombre, 
    p.fecha_pedido, 
    ROUND(SUM(dp.cantidad * dp.precio_unitario), 2) AS total
FROM clientes AS c
JOIN pedidos AS p 
    ON c.cliente_id = p.cliente_id
JOIN detalle_pedidos AS dp 
    ON p.pedido_id = dp.pedido_id

WHERE p.estado = 'completado'
GROUP BY 
    c.nombre, 
    p.pedido_id, 
    p.fecha_pedido
ORDER BY total DESC
LIMIT 10;

-- Ejercicio 07
-- Clientes cuyo gasto total (pedidos completados) es MAYOR que el gasto promedio
-- de todos los clientes que han comprado algo completado. Columnas:
-- cliente_id, nombre, gasto_total (redondeado a 2 decimales)
-- Conceptos: CTE (WITH ...), subconsulta escalar

-- Escribe tu consulta aquí:
SELECT 
    c.cliente_id, 
    c.nombre, 
    SUM(dp.precio_unitario) AS total
FROM clientes AS c
JOIN pedidos AS p 
    ON c.cliente_id = p.cliente_id
JOIN detalle_pedidos AS dp 
    ON dp.pedido_id = p.pedido_id
WHERE p.estado = 'completado'
GROUP BY c.cliente_id, c.nombre
HAVING SUM(dp.precio_unitario) > (
    SELECT AVG(precio_unitario) FROM detalle_pedidos
)

ORDER BY c.cliente_id;

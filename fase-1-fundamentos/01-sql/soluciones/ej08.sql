WITH ingresos_producto AS (
    SELECT pr.producto_id, pr.categoria, pr.nombre AS producto,
           SUM(d.cantidad * d.precio_unitario) AS ingresos
    FROM detalle_pedidos d
    JOIN pedidos p    ON p.pedido_id = d.pedido_id
    JOIN productos pr ON pr.producto_id = d.producto_id
    WHERE p.estado = 'completado'
    GROUP BY pr.producto_id, pr.categoria, pr.nombre
),
ranking AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY ingresos DESC, producto_id) AS posicion
    FROM ingresos_producto
)
SELECT categoria, producto, ROUND(ingresos, 2) AS ingresos, posicion
FROM ranking
WHERE posicion <= 3;

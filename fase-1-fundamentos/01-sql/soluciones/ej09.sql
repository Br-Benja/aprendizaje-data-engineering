WITH mensual AS (
    SELECT DATE_TRUNC('month', p.fecha_pedido) AS mes,
           SUM(d.cantidad * d.precio_unitario) AS ingresos
    FROM pedidos p
    JOIN detalle_pedidos d ON d.pedido_id = p.pedido_id
    WHERE p.estado = 'completado'
    GROUP BY mes
),
con_anterior AS (
    SELECT mes, ingresos, LAG(ingresos) OVER (ORDER BY mes) AS anterior
    FROM mensual
)
SELECT mes,
       ROUND(ingresos, 2) AS ingresos,
       ROUND(anterior, 2) AS ingresos_mes_anterior,
       ROUND((ingresos - anterior) / anterior * 100, 2) AS crecimiento_pct
FROM con_anterior
ORDER BY mes;

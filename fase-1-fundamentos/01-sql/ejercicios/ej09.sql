-- Ejercicio 09
-- Crecimiento mes a mes de los ingresos (pedidos completados, TODOS los meses). Columnas:
-- mes, ingresos, ingresos_mes_anterior, crecimiento_pct
-- crecimiento_pct = (ingresos - anterior) / anterior * 100, redondeado a 2 decimales.
-- El primer mes no tiene anterior -> NULL.  Ordena por mes.
-- Conceptos: LAG()

-- Escribe tu consulta aquí:

WITH ingresos_mensuales AS (
    SELECT
        DATE_TRUNC('month', p.fecha_pedido) AS mes,
        SUM(dp.cantidad * dp.precio_unitario) AS ingresos
    FROM pedidos AS p
    JOIN detalle_pedidos AS dp
        ON dp.pedido_id = p.pedido_id
    WHERE p.estado = 'completado'
    GROUP BY mes
),

comparacion AS (
    SELECT
        mes,
        ingresos,
        LAG(ingresos) OVER (
            ORDER BY mes
        ) AS ingresos_mes_anterior
    FROM ingresos_mensuales
)

SELECT
    mes,
    ingresos,
    ingresos_mes_anterior,
    ROUND(
    (ingresos - ingresos_mes_anterior) /
    NULLIF(ingresos_mes_anterior, 0) * 100,
    2
) AS crecimiento_pct
FROM comparacion
ORDER BY mes;
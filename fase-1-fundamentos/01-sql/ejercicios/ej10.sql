-- Ejercicio 10
-- Para CADA pedido (cualquier estado) calcula cuántos días pasaron desde el pedido
-- anterior del MISMO cliente. Columnas:
-- cliente_id, pedido_id, fecha_pedido, dias_desde_anterior (entero; NULL en su primer pedido)
-- El 'anterior' se define ordenando por fecha_pedido y luego pedido_id.
-- Conceptos: LAG() con PARTITION BY, resta de fechas

-- Escribe tu consulta aquí:

SELECT
    cliente_id,
    pedido_id,
    fecha_pedido,

    DATE_DIFF(
        'day',
        fecha_anterior,
        fecha_pedido
    ) AS dias_desde_anterior

FROM (
    SELECT
        cliente_id,
        pedido_id,
        fecha_pedido,

        LAG(fecha_pedido) OVER (
            PARTITION BY cliente_id
            ORDER BY fecha_pedido, pedido_id
        ) AS fecha_anterior

    FROM pedidos
) AS pedidos_ordenados

ORDER BY cliente_id, fecha_pedido, pedido_id;
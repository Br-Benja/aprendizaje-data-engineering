-- Ejercicio 08
-- Top 3 productos por ingresos DENTRO de cada categoría (solo pedidos completados). Columnas:
-- categoria, producto (nombre del producto), ingresos (2 decimales), posicion (1, 2 o 3)
-- Si hay empate, desempata por producto_id menor.
-- Conceptos: window functions -> ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)

-- Escribe tu consulta aquí:

falta 

WITH ingresos AS (
    SELECT 
        pr.producto_id,
        pr.nombre,
        pr.categoria,
        SUM(dp.cantidad * dp.precio_unitario) AS Total,
        ROW_NUMBER() OVER (
            PARTITION BY pr.categoria
            ORDER BY SUM(dp.cantidad * dp.precio_unitario) DESC, pr.producto_id
        ) AS enumeracion
    FROM detalle_pedidos AS dp
    JOIN producto AS pr 
        ON pr.producto_id = dp.producto_id
    JOIN pedidos AS pd
        ON pd.pedido_id = dp.pedido_id
    WHERE pd.estado = 'completado'
    GROUP BY pr.producto_id, pr.nombre, pr.categoria
)
SELECT 
    producto_id,
    nombre,
    categoria,
    ROUND(Total, 2) AS ingresos
FROM ingresos
WHERE enumeracion <= 3;

-- Ejercicio 06
-- Ingresos por mes durante 2025 (solo pedidos completados). Columnas:
-- mes             -> DATE_TRUNC('month', fecha_pedido)
-- ingresos        -> SUM(cantidad * precio_unitario) redondeado a 2 decimales
-- numero_pedidos  -> cantidad de pedidos distintos
-- Ordena por mes.
-- Conceptos: funciones de fecha, COUNT(DISTINCT ...)

-- Escribe tu consulta aquí: 


select DATE_TRUNC('month',fecha_pedido) as mes, 
ROUND(SUM(dp.cantidad * dp.precio_unitario),2) as TOTAL, 
COUNT(DISTINCT dp.pedido_id)
from pedidos as p 
JOIN detalle_pedidos as dp 
ON dp.pedido_id = p.pedido_id 
WHERE p.estado = 'completado' AND p.fecha_pedido >= DATE '2025-01-01' AND p.fecha_pedido <= DATE '2026-01-01'  
GROUP BY mes 
ORDER BY mes;
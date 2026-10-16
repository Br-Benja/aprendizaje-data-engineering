-- Ejercicio 10
-- Para CADA pedido (cualquier estado) calcula cuántos días pasaron desde el pedido
-- anterior del MISMO cliente. Columnas:
-- cliente_id, pedido_id, fecha_pedido, dias_desde_anterior (entero; NULL en su primer pedido)
-- El 'anterior' se define ordenando por fecha_pedido y luego pedido_id.
-- Conceptos: LAG() con PARTITION BY, resta de fechas

-- Escribe tu consulta aquí:


-- Ejercicio 02
-- Para cada categoría muestra: categoria, numero_productos, precio_promedio
-- (precio_promedio redondeado a 2 decimales con ROUND).
-- Conceptos: GROUP BY, COUNT, AVG

-- Escribe tu consulta aquí:
select categoria,
COUNT(categoria) as numero_productos,
ROUND(AVG(precio),2) as precio_promedio 
from productos 
group by categoria;


-- Ejercicio 05
-- Clientes que NUNCA han hecho un pedido (de ningÃºn estado): cliente_id, nombre, pais.
-- Conceptos: LEFT JOIN + IS NULL (o NOT EXISTS)

-- Escribe tu consulta aquÃ­:

select c.cliente_id, c.nombre, c.pais 
from clientes as c 
left join pedidos as p 
on p.cliente_id = c.cliente_id 
where p.pedido_id is null;
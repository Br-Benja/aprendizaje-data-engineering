-- Ejercicio 01
-- Lista los clientes de 'México' con: cliente_id, nombre, ciudad, fecha_registro.
-- Ordena por fecha_registro y luego por cliente_id.
-- Conceptos: SELECT, WHERE, ORDER BY

-- Escribe tu consulta aquí:

select * from clientes, Where pais = 'México' order by fecha_registro;
select * from clientes, Where pais = 'México' order by cliente_id;    

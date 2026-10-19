-- Ejercicio 03
-- Muestra solo las categorÃ­as que tienen MÃS de 6 productos: categoria, numero_productos.
-- Conceptos: HAVING (filtrar despuÃ©s de agrupar)

-- Escribe tu consulta aquÃ­:

select categoria, 
count(categoria) as numero_productos 
from productos 
group by categoria, 
having count(categoria)>6 ; 
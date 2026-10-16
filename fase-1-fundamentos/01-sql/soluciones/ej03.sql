SELECT categoria, COUNT(*) AS numero_productos
FROM productos
GROUP BY categoria
HAVING COUNT(*) > 6;

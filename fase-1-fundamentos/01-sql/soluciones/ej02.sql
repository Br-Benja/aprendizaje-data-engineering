SELECT categoria,
       COUNT(*)              AS numero_productos,
       ROUND(AVG(precio), 2) AS precio_promedio
FROM productos
GROUP BY categoria;

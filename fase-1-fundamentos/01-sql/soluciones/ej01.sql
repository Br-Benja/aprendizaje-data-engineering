SELECT cliente_id, nombre, ciudad, fecha_registro
FROM clientes
WHERE pais = 'México'
ORDER BY fecha_registro, cliente_id;

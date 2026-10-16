"""Genera la base de datos de práctica `tienda.duckdb` (una tienda en línea ficticia).

Uso:  py generar_datos.py
Los datos son aleatorios pero reproducibles (semilla fija), así todos obtienen los mismos resultados.
"""
import random
from datetime import date, timedelta
from pathlib import Path

import duckdb

random.seed(42)
RUTA_DB = Path(__file__).parent / "tienda.duckdb"

NOMBRES = ["Ana", "Luis", "María", "Carlos", "Sofía", "Jorge", "Lucía", "Pedro", "Valeria", "Diego",
           "Camila", "Andrés", "Daniela", "Miguel", "Paula", "Javier", "Elena", "Raúl", "Isabel", "Tomás"]
APELLIDOS = ["García", "Martínez", "López", "Hernández", "González", "Pérez", "Rodríguez", "Sánchez",
             "Ramírez", "Torres", "Flores", "Rivera", "Gómez", "Díaz", "Vargas", "Castro"]
CIUDADES = {
    "México": ["CDMX", "Guadalajara", "Monterrey", "Puebla"],
    "Colombia": ["Bogotá", "Medellín", "Cali"],
    "Argentina": ["Buenos Aires", "Córdoba", "Rosario"],
    "Chile": ["Santiago", "Valparaíso"],
    "Perú": ["Lima", "Arequipa"],
    "España": ["Madrid", "Barcelona", "Valencia"],
}
CATALOGO = {
    "Electrónica": [("Audífonos", 35, 180), ("Teclado mecánico", 45, 150), ("Mouse inalámbrico", 15, 60),
                    ("Monitor 27\"", 180, 420), ("Webcam HD", 30, 110), ("Disco SSD 1TB", 60, 140),
                    ("Hub USB-C", 20, 70), ("Bocina Bluetooth", 25, 130)],
    "Hogar": [("Cafetera", 40, 200), ("Lámpara de escritorio", 18, 75), ("Silla ergonómica", 120, 380),
              ("Organizador", 10, 35), ("Termo", 12, 45), ("Juego de sartenes", 50, 160)],
    "Libros": [("Fundamentals of Data Engineering", 35, 55), ("Designing Data-Intensive Applications", 40, 60),
               ("Clean Code", 30, 50), ("Python Crash Course", 25, 45), ("SQL Cookbook", 30, 50),
               ("The Pragmatic Programmer", 30, 55), ("Storytelling with Data", 25, 45)],
    "Deportes": [("Tapete de yoga", 15, 50), ("Mancuernas 10kg", 30, 90), ("Botella deportiva", 8, 25),
                 ("Bicicleta estática", 200, 550), ("Cuerda para saltar", 6, 20), ("Mochila", 25, 85)],
    "Ropa": [("Sudadera", 25, 70), ("Playera técnica", 12, 35), ("Tenis para correr", 50, 160),
             ("Chamarra", 45, 150), ("Gorra", 10, 30)],
}

INICIO, FIN = date(2024, 1, 1), date(2025, 12, 31)


def fecha_aleatoria(desde: date, hasta: date) -> date:
    return desde + timedelta(days=random.randint(0, (hasta - desde).days))


def generar():
    clientes = []
    for cid in range(1, 201):
        pais = random.choice(list(CIUDADES))
        ciudad = random.choice(CIUDADES[pais]) if random.random() > 0.05 else None  # algunos sin ciudad
        nombre = f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}"
        clientes.append((cid, nombre, ciudad, pais, fecha_aleatoria(INICIO - timedelta(days=365), FIN)))

    productos, pid = [], 1
    for categoria, items in CATALOGO.items():
        for nombre, minimo, maximo in items:
            productos.append((pid, nombre, categoria, round(random.uniform(minimo, maximo), 2)))
            pid += 1
    precios = {p[0]: p[3] for p in productos}

    # ~15% de los clientes nunca compra (útil para practicar LEFT JOIN)
    compradores = [c for c in clientes if random.random() > 0.15]
    pedidos, detalle = [], []
    for pedido_id in range(1, 2001):
        cliente = random.choice(compradores)
        fecha = fecha_aleatoria(max(cliente[4], INICIO), FIN)  # nunca antes de que se registre
        estado = random.choices(["completado", "cancelado", "pendiente"], weights=[82, 10, 8])[0]
        pedidos.append((pedido_id, cliente[0], fecha, estado))
        for producto_id in random.sample(list(precios), k=random.choices([1, 2, 3, 4], weights=[45, 30, 15, 10])[0]):
            # el precio cobrado puede tener descuento respecto al de lista
            precio = round(precios[producto_id] * random.choice([1, 1, 1, 0.9, 0.85]), 2)
            detalle.append((pedido_id, producto_id, random.choices([1, 2, 3], weights=[75, 20, 5])[0], precio))
    return clientes, productos, pedidos, detalle


def main():
    clientes, productos, pedidos, detalle = generar()
    RUTA_DB.unlink(missing_ok=True)
    con = duckdb.connect(str(RUTA_DB))
    con.execute("""
        CREATE TABLE clientes (cliente_id INTEGER PRIMARY KEY, nombre VARCHAR, ciudad VARCHAR,
                               pais VARCHAR, fecha_registro DATE);
        CREATE TABLE productos (producto_id INTEGER PRIMARY KEY, nombre VARCHAR, categoria VARCHAR,
                                precio DECIMAL(10, 2));
        CREATE TABLE pedidos (pedido_id INTEGER PRIMARY KEY, cliente_id INTEGER REFERENCES clientes,
                              fecha_pedido DATE, estado VARCHAR);
        CREATE TABLE detalle_pedidos (pedido_id INTEGER REFERENCES pedidos,
                                      producto_id INTEGER REFERENCES productos,
                                      cantidad INTEGER, precio_unitario DECIMAL(10, 2));
    """)
    con.executemany("INSERT INTO clientes VALUES (?, ?, ?, ?, ?)", clientes)
    con.executemany("INSERT INTO productos VALUES (?, ?, ?, ?)", productos)
    con.executemany("INSERT INTO pedidos VALUES (?, ?, ?, ?)", pedidos)
    con.executemany("INSERT INTO detalle_pedidos VALUES (?, ?, ?, ?)", detalle)
    for tabla in ["clientes", "productos", "pedidos", "detalle_pedidos"]:
        print(f"{tabla:<16} {con.sql(f'SELECT COUNT(*) FROM {tabla}').fetchone()[0]:>6} filas")
    con.close()
    print(f"\nBase creada en {RUTA_DB.name}")


if __name__ == "__main__":
    main()

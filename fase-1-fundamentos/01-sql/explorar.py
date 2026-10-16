"""Ejecuta una consulta libre sobre tienda.duckdb para explorar los datos.

Uso:
    py explorar.py "SELECT * FROM clientes LIMIT 5"
    py explorar.py ejercicios/ej04.sql
    py explorar.py                      -> modo interactivo (escribe consultas, 'salir' para terminar)
"""
import sys
from pathlib import Path

import duckdb

sys.stdout.reconfigure(encoding="utf-8")
RUTA_DB = Path(__file__).parent / "tienda.duckdb"


def ejecutar(con, sql: str):
    try:
        relacion = con.sql(sql)
        if relacion is not None:
            relacion.show(max_rows=30)
    except duckdb.Error as e:
        print(f"Error: {e}")


def main():
    con = duckdb.connect(str(RUTA_DB), read_only=True)
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        ejecutar(con, Path(arg).read_text(encoding="utf-8-sig") if arg.endswith(".sql") else arg)
        return
    print("Modo interactivo. Termina cada consulta con ';'. Escribe 'salir' para terminar.")
    buffer = ""
    while (linea := input("sql> " if not buffer else "...> ")).strip().lower() != "salir":
        buffer += linea + "\n"
        if buffer.strip().endswith(";"):
            ejecutar(con, buffer)
            buffer = ""


if __name__ == "__main__":
    main()

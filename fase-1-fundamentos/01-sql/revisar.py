"""Revisa tus respuestas comparándolas con el resultado esperado.

Uso:
    py revisar.py        -> revisa todos los ejercicios
    py revisar.py 4      -> revisa solo el ejercicio 4 y muestra tu resultado
"""
import sys
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import duckdb

sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).parent
RUTA_DB = AQUI / "tienda.duckdb"
ORDEN_IMPORTA = {1, 4, 6, 9}  # ejercicios donde se pide un ORDER BY específico
TOLERANCIA = 0.02


def normalizar(valor):
    if isinstance(valor, (Decimal, float)):
        return round(float(valor), 2)
    if isinstance(valor, (date, datetime)):
        return valor.strftime("%Y-%m-%d")
    return valor


def clave_orden(fila):
    return tuple(str(round(v)) if isinstance(v, float) else str(v) for v in fila)


def filas_iguales(a, b):
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool):
            if abs(x - y) > TOLERANCIA:
                return False
        elif x != y:
            return False
    return True


def tiene_consulta(sql: str) -> bool:
    return any(l.strip() and not l.strip().startswith("--") for l in sql.splitlines())


def revisar(con, n: int, detalle: bool) -> bool:
    archivo = f"ej{n:02d}.sql"
    sql_tuyo = (AQUI / "ejercicios" / archivo).read_text(encoding="utf-8-sig")
    if not tiene_consulta(sql_tuyo):
        print(f"⬜ Ejercicio {n:02d}: sin responder")
        return False
    esperado = [tuple(map(normalizar, f)) for f in con.sql((AQUI / "soluciones" / archivo).read_text(encoding="utf-8")).fetchall()]
    try:
        relacion = con.sql(sql_tuyo)
        if relacion is None:
            print(f"❌ Ejercicio {n:02d}: la consulta no devuelve filas (¿falta un SELECT?)")
            return False
        tuyo = [tuple(map(normalizar, f)) for f in relacion.fetchall()]
    except duckdb.Error as e:
        print(f"💥 Ejercicio {n:02d}: error de SQL\n   {e}")
        return False

    if n not in ORDEN_IMPORTA:
        esperado.sort(key=clave_orden)
        tuyo.sort(key=clave_orden)

    if len(tuyo) != len(esperado):
        motivo = f"devuelve {len(tuyo)} filas y se esperaban {len(esperado)}"
    elif tuyo and len(tuyo[0]) != len(esperado[0]):
        motivo = f"devuelve {len(tuyo[0])} columnas y se esperaban {len(esperado[0])}"
    elif not all(filas_iguales(a, b) for a, b in zip(tuyo, esperado)):
        i = next(i for i, (a, b) in enumerate(zip(tuyo, esperado)) if not filas_iguales(a, b))
        motivo = f"la fila {i + 1} no coincide\n   tuya:     {tuyo[i]}\n   esperada: {esperado[i]}"
    else:
        print(f"✅ Ejercicio {n:02d}: ¡correcto!")
        return True

    print(f"❌ Ejercicio {n:02d}: {motivo}")
    if detalle:
        print("\nTu resultado (primeras filas):")
        con.sql(sql_tuyo).show(max_rows=10)
    return False


def main():
    if not RUTA_DB.exists():
        sys.exit("No existe tienda.duckdb. Primero ejecuta:  py generar_datos.py")
    con = duckdb.connect(str(RUTA_DB), read_only=True)
    numeros = [int(sys.argv[1])] if len(sys.argv) > 1 else range(1, 11)
    correctos = sum(revisar(con, n, detalle=len(numeros) == 1) for n in numeros)
    if len(numeros) > 1:
        print(f"\nResultado: {correctos}/{len(numeros)} correctos")


if __name__ == "__main__":
    main()

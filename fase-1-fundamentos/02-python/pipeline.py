"""Mini pipeline ETL de clima: API de Open-Meteo → limpieza con pandas → archivos Parquet.

Tu trabajo: completar las 7 funciones marcadas con TODO.
Revisa tu avance con:   py -m pytest -v            (todos)
                        py -m pytest -v -k ej3     (solo el ejercicio 3)
Cuando todos pasen:     py pipeline.py             (corre el pipeline con datos reales)
"""
import json
import logging
from pathlib import Path

import pandas as pd
import requests

URL_API = "https://archive-api.open-meteo.com/v1/archive"
VARIABLES = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]

log = logging.getLogger("pipeline_clima")


# ============================================================== EXTRACT
def construir_parametros(latitud: float, longitud: float, inicio: str, fin: str) -> dict:
    """EJERCICIO 1 — Arma el diccionario de parámetros para la API.

    Debe tener exactamente estas llaves:
      latitude, longitude, start_date, end_date  -> los argumentos recibidos
      daily     -> los elementos de VARIABLES unidos por comas: "temperature_2m_max,temperature_2m_min,..."
      timezone  -> "America/Mexico_City"
    Pista: ",".join(lista)
    """
    return {
        "latitude": latitud,
        "longitude" : longitud,
        "start_date" : inicio,
        "end_date" : fin, 
        "daily": ",".join(VARIABLES),
        "timezone" : "America/Mexico_City"
    }


def extraer(latitud: float, longitud: float, inicio: str, fin: str) -> dict:
    """EJERCICIO 7 (déjalo para el final) — Llama a la API y regresa el JSON como dict.

    - Usa requests.get(URL_API, params=..., timeout=30)   ← SIEMPRE pon timeout en producción
    - Llama a .raise_for_status() para que un error HTTP (404, 500) lance excepción
    - Regresa .json()
    """
    respuesta = requests.get( 
        URL_API,
        params = construir_parametros(latitud,longitud, inicio, fin),
        timeout = 30
    )
    respuesta.raise_for_status()
    return respuesta.json()




# ============================================================== TRANSFORM
def a_dataframe(respuesta: dict) -> pd.DataFrame:
    """EJERCICIO 2 — Convierte la respuesta de la API en un DataFrame.

    La respuesta se ve así:
      {"daily": {"time": ["2025-01-01", ...],
                 "temperature_2m_max": [26.4, ...],
                 "temperature_2m_min": [8.1, ...],
                 "precipitation_sum": [0.0, ...]}, ...}

    Columnas resultantes, en este orden:
      fecha (tipo datetime, usa pd.to_datetime), temp_max, temp_min, precipitacion
    """
    data = respuesta["daily"]
    return pd.DataFrame({
        "fecha" : pd.to_datetime(data["time"]),
        "temp_max" : data["temperature_2m_max"],
        "temp_min" : data["temperature_2m_min"],
        "precipitacion" : data["precipitation_sum"]
    })


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """EJERCICIO 3 — Limpia los datos (¡los datos reales siempre vienen sucios!).

    1. Elimina filas donde temp_max o temp_min sean nulas         -> dropna(subset=...)
    2. Si precipitacion es nula, rellénala con 0.0                 -> fillna(...)
    3. Si una fecha está repetida, quédate con la ÚLTIMA aparición -> drop_duplicates(..., keep="last")
    4. Ordena por fecha y reinicia el índice                       -> sort_values / reset_index(drop=True)
    """
    limpio = ( 
        df
        .dropna(subset=["temp_max","temp_min"])
        .fillna({"precipitacion" : 0.0})
        .drop_duplicates(subset="fecha", keep = "last")
        .sort_values("fecha")
        .reset_index(drop = True)
    )
    return limpio

def agregar_columnas(df: pd.DataFrame, ciudad: str) -> pd.DataFrame:
    """EJERCICIO 4 — Agrega columnas calculadas (sin modificar el df original: usa df.copy()).

      temp_promedio -> (temp_max + temp_min) / 2, redondeado a 1 decimal
      llovio        -> True si precipitacion > 0
      ciudad        -> el nombre recibido
    """
    df = df.copy()
    df["temp_promedio"] = ((df["temp_max"] + df["temp_min"])/2).round(1)
    df["llovio"] = df["precipitacion"] > 0
    df["ciudad"] = ciudad

    return df

def resumen_mensual(df: pd.DataFrame) -> pd.DataFrame:
    """EJERCICIO 5 — El GROUP BY de pandas. Recibe el df con las columnas del ejercicio 4.

    Columnas resultantes, en este orden:
      ciudad, mes (texto "YYYY-MM", usa .dt.strftime("%Y-%m")),
      temp_promedio (promedio, 1 decimal), precipitacion_total (suma, 1 decimal),
      dias_lluvia (cuántos días llovió, entero)
    Ordenado por ciudad y mes, con índice reiniciado.
    Pista: df.groupby([...], as_index=False).agg(nombre=("columna", "funcion"), ...)
    """
    resumen = (
        df
        .assign(mes = df["fecha"].dt.strftime("%Y-%m"))
        .groupby(["ciudad", "mes"], as_index = False)
        .agg(
            temp_promedio = ("temp_promedio", "mean"),
            precipitacion_total = ("precipitacion", "sum"),
            dias_lluvia = ("llovio", "sum"),
        )
        .round({"temp_promedio" : 1, "precipitacion_total" : 1})
        .sort_values(["ciudad", "mes"])
        .reset_index(drop=True)
    )

    return resumen


# ============================================================== LOAD
def guardar_parquet(df: pd.DataFrame, ruta: Path) -> None:
    """EJERCICIO 6 — Guarda el DataFrame en formato Parquet.

    - Crea la carpeta si no existe: ruta.parent.mkdir(parents=True, exist_ok=True)
    - No guardes el índice: index=False
    - Correrlo dos veces debe dar el mismo resultado (sobrescribir, no duplicar) = IDEMPOTENCIA
    """

    ruta = Path(ruta)
    ruta.parent.mkdir(parents = True, exist_ok=True)
    df.to_parquet(ruta, index=False)




# ============================================================== ORQUESTACIÓN (ya está hecha)
CIUDADES = {
    "Celaya": (20.52, -100.81),
    "CDMX": (19.43, -99.13),
    "Monterrey": (25.67, -100.31),
}
CARPETA_DATOS = Path(__file__).parent / "datos"


def main(inicio: str = "2025-01-01", fin: str = "2025-12-31"):
    import duckdb
    import truststore

    truststore.inject_into_ssl()  # usa los certificados de Windows (evita errores SSL con antivirus/proxys)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-7s %(message)s")

    tablas = []
    for ciudad, (lat, lon) in CIUDADES.items():
        log.info("Extrayendo %s (%s a %s)", ciudad, inicio, fin)
        crudo = extraer(lat, lon, inicio, fin)

        # Capa "cruda": guardamos tal cual llegó, por si necesitamos reprocesar sin volver a llamar a la API
        ruta_cruda = CARPETA_DATOS / "crudo" / f"{ciudad.lower()}_{inicio}_{fin}.json"
        ruta_cruda.parent.mkdir(parents=True, exist_ok=True)
        ruta_cruda.write_text(json.dumps(crudo), encoding="utf-8")

        df = agregar_columnas(limpiar(a_dataframe(crudo)), ciudad)
        log.info("%s: %d días limpios", ciudad, len(df))
        tablas.append(df)

    diario = pd.concat(tablas, ignore_index=True)
    guardar_parquet(diario, CARPETA_DATOS / "procesado" / "clima_diario.parquet")
    guardar_parquet(resumen_mensual(diario), CARPETA_DATOS / "procesado" / "resumen_mensual.parquet")
    log.info("Archivos Parquet guardados en %s", CARPETA_DATOS / "procesado")

    # ¡DuckDB puede consultar archivos Parquet directamente con SQL! (lo que aprendiste en la lección 01)
    print("\nCiudad más lluviosa por mes:")
    duckdb.sql(f"""
        SELECT mes, ciudad, precipitacion_total
        FROM '{(CARPETA_DATOS / "procesado" / "resumen_mensual.parquet").as_posix()}'
        QUALIFY ROW_NUMBER() OVER (PARTITION BY mes ORDER BY precipitacion_total DESC) = 1
        ORDER BY mes
    """).show()


if __name__ == "__main__":
    main()

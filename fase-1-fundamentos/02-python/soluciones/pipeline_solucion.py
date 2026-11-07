"""Solución de referencia de la Lección 02. ¡No la abras hasta que tus tests pasen!"""
import logging
from pathlib import Path

import pandas as pd
import requests

URL_API = "https://archive-api.open-meteo.com/v1/archive"
VARIABLES = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]

log = logging.getLogger("pipeline_clima")


# ---------------------------------------------------------------- EXTRACT
def construir_parametros(latitud: float, longitud: float, inicio: str, fin: str) -> dict:
    return {
        "latitude": latitud,
        "longitude": longitud,
        "start_date": inicio,
        "end_date": fin,
        "daily": ",".join(VARIABLES),
        "timezone": "America/Mexico_City",
    }


def extraer(latitud: float, longitud: float, inicio: str, fin: str) -> dict:
    respuesta = requests.get(URL_API, params=construir_parametros(latitud, longitud, inicio, fin), timeout=30)
    respuesta.raise_for_status()
    return respuesta.json()


# ---------------------------------------------------------------- TRANSFORM
def a_dataframe(respuesta: dict) -> pd.DataFrame:
    diario = respuesta["daily"]
    return pd.DataFrame({
        "fecha": pd.to_datetime(diario["time"]),
        "temp_max": diario["temperature_2m_max"],
        "temp_min": diario["temperature_2m_min"],
        "precipitacion": diario["precipitation_sum"],
    })


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.dropna(subset=["temp_max", "temp_min"])
          .fillna({"precipitacion": 0.0})
          .drop_duplicates(subset="fecha", keep="last")
          .sort_values("fecha")
          .reset_index(drop=True)
    )


def agregar_columnas(df: pd.DataFrame, ciudad: str) -> pd.DataFrame:
    df = df.copy()
    df["temp_promedio"] = ((df["temp_max"] + df["temp_min"]) / 2).round(1)
    df["llovio"] = df["precipitacion"] > 0
    df["ciudad"] = ciudad
    return df


def resumen_mensual(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.assign(mes=df["fecha"].dt.strftime("%Y-%m"))
          .groupby(["ciudad", "mes"], as_index=False)
          .agg(temp_promedio=("temp_promedio", "mean"),
               precipitacion_total=("precipitacion", "sum"),
               dias_lluvia=("llovio", "sum"))
          .round({"temp_promedio": 1, "precipitacion_total": 1})
          .astype({"dias_lluvia": int})
          .sort_values(["ciudad", "mes"])
          .reset_index(drop=True)
    )


# ---------------------------------------------------------------- LOAD
def guardar_parquet(df: pd.DataFrame, ruta: Path) -> None:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(ruta, index=False)

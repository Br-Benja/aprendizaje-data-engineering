"""Tests de la Lección 02. NO los modifiques: tu código debe hacerlos pasar.

Ejecuta desde la carpeta 02-python:   py -m pytest -v
"""
import pandas as pd
import pytest

import pipeline

RESPUESTA_FALSA = {
    "latitude": 20.5,
    "longitude": -100.8,
    "daily": {
        "time": ["2025-01-01", "2025-01-02", "2025-01-03"],
        "temperature_2m_max": [26.4, 25.2, 24.0],
        "temperature_2m_min": [8.1, 8.3, 7.5],
        "precipitation_sum": [0.0, 1.5, 0.0],
    },
}


def df_sucio():
    """Datos con los problemas típicos: desorden, duplicados y nulos."""
    return pd.DataFrame({
        "fecha": pd.to_datetime(["2025-01-03", "2025-01-01", "2025-01-02", "2025-01-02", "2025-01-04"]),
        "temp_max": [24.0, 26.4, 99.9, 25.2, None],
        "temp_min": [7.5, 8.1, 99.9, 8.3, 6.0],
        "precipitacion": [None, 0.0, 0.0, 1.5, 0.0],
    })


def df_enriquecido():
    return pd.DataFrame({
        "fecha": pd.to_datetime(["2025-01-30", "2025-01-31", "2025-02-01", "2025-01-15"]),
        "temp_max": [20.0, 22.0, 30.0, 18.0],
        "temp_min": [10.0, 12.0, 14.0, 6.0],
        "precipitacion": [2.24, 0.0, 5.0, 0.0],
        "temp_promedio": [15.0, 17.0, 22.0, 12.0],
        "llovio": [True, False, True, False],
        "ciudad": ["Celaya", "Celaya", "Celaya", "CDMX"],
    })


# ------------------------------------------------------------------ Ejercicio 1
def test_ej1_parametros():
    params = pipeline.construir_parametros(20.5, -100.8, "2025-01-01", "2025-01-31")
    assert params == {
        "latitude": 20.5,
        "longitude": -100.8,
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "America/Mexico_City",
    }


# ------------------------------------------------------------------ Ejercicio 2
def test_ej2_columnas_y_orden():
    df = pipeline.a_dataframe(RESPUESTA_FALSA)
    assert list(df.columns) == ["fecha", "temp_max", "temp_min", "precipitacion"]
    assert len(df) == 3


def test_ej2_fecha_es_datetime():
    df = pipeline.a_dataframe(RESPUESTA_FALSA)
    assert pd.api.types.is_datetime64_any_dtype(df["fecha"]), "fecha debe ser datetime, usa pd.to_datetime"
    assert df.loc[1, "precipitacion"] == 1.5


# ------------------------------------------------------------------ Ejercicio 3
def test_ej3_elimina_nulos_y_duplicados():
    df = pipeline.limpiar(df_sucio())
    assert len(df) == 3, "deben quedar 3 días: se quita el nulo del 04 y el 02 duplicado"
    assert df["temp_max"].isna().sum() == 0


def test_ej3_duplicado_conserva_el_ultimo():
    df = pipeline.limpiar(df_sucio())
    fila = df[df["fecha"] == "2025-01-02"].iloc[0]
    assert fila["temp_max"] == 25.2, "con fechas repetidas se conserva la ÚLTIMA aparición"


def test_ej3_ordena_rellena_y_reinicia_indice():
    df = pipeline.limpiar(df_sucio())
    assert list(df["fecha"].dt.day) == [1, 2, 3]
    assert list(df.index) == [0, 1, 2]
    assert df["precipitacion"].isna().sum() == 0, "precipitación nula debe volverse 0.0"


def test_ej3_no_modifica_el_original():
    original = df_sucio()
    pipeline.limpiar(original)
    assert len(original) == 5


# ------------------------------------------------------------------ Ejercicio 4
def test_ej4_columnas_nuevas():
    base = pd.DataFrame({
        "fecha": pd.to_datetime(["2025-01-01", "2025-01-02"]),
        "temp_max": [26.0, 25.0],
        "temp_min": [8.4, 8.0],
        "precipitacion": [0.0, 1.5],
    })
    df = pipeline.agregar_columnas(base, "Celaya")
    assert list(df["temp_promedio"]) == [17.2, 16.5]
    assert list(df["llovio"]) == [False, True]
    assert (df["ciudad"] == "Celaya").all()


def test_ej4_no_modifica_el_original():
    base = pd.DataFrame({"fecha": pd.to_datetime(["2025-01-01"]), "temp_max": [20.0],
                         "temp_min": [10.0], "precipitacion": [0.0]})
    pipeline.agregar_columnas(base, "CDMX")
    assert "ciudad" not in base.columns, "usa df.copy() para no modificar el DataFrame recibido"


# ------------------------------------------------------------------ Ejercicio 5
def test_ej5_resumen_mensual():
    res = pipeline.resumen_mensual(df_enriquecido())
    assert list(res.columns) == ["ciudad", "mes", "temp_promedio", "precipitacion_total", "dias_lluvia"]
    assert list(res["ciudad"]) == ["CDMX", "Celaya", "Celaya"], "ordena por ciudad y luego por mes"
    assert list(res["mes"]) == ["2025-01", "2025-01", "2025-02"]


def test_ej5_valores():
    res = pipeline.resumen_mensual(df_enriquecido())
    enero_celaya = res[(res["ciudad"] == "Celaya") & (res["mes"] == "2025-01")].iloc[0]
    assert enero_celaya["temp_promedio"] == 16.0
    assert enero_celaya["precipitacion_total"] == 2.2  # 2.24 redondeado a 1 decimal
    assert enero_celaya["dias_lluvia"] == 1
    assert list(res.index) == [0, 1, 2]


# ------------------------------------------------------------------ Ejercicio 6
def test_ej6_guarda_y_se_puede_leer(tmp_path):
    ruta = tmp_path / "sub" / "carpeta" / "datos.parquet"  # carpetas que aún no existen
    df = df_enriquecido()
    pipeline.guardar_parquet(df, ruta)
    leido = pd.read_parquet(ruta)
    pd.testing.assert_frame_equal(leido, df)


def test_ej6_es_idempotente(tmp_path):
    ruta = tmp_path / "datos.parquet"
    pipeline.guardar_parquet(df_enriquecido(), ruta)
    pipeline.guardar_parquet(df_enriquecido(), ruta)  # correrlo de nuevo NO debe duplicar
    assert len(pd.read_parquet(ruta)) == 4


# ------------------------------------------------------------------ Ejercicio 7
class RespuestaFalsa:
    def __init__(self, codigo=200):
        self.codigo = codigo

    def raise_for_status(self):
        if self.codigo >= 400:
            raise pipeline.requests.HTTPError(f"Error {self.codigo}")

    def json(self):
        return RESPUESTA_FALSA


def test_ej7_extraer_llama_a_la_api(monkeypatch):
    llamadas = []

    def get_falso(url, params=None, timeout=None, **kwargs):
        llamadas.append({"url": url, "params": params, "timeout": timeout})
        return RespuestaFalsa()

    monkeypatch.setattr(pipeline.requests, "get", get_falso)  # así probamos sin internet
    resultado = pipeline.extraer(20.5, -100.8, "2025-01-01", "2025-01-31")

    assert resultado == RESPUESTA_FALSA
    assert llamadas[0]["url"] == pipeline.URL_API
    assert llamadas[0]["params"]["start_date"] == "2025-01-01", "usa construir_parametros para los params"
    assert llamadas[0]["timeout"] is not None, "¡siempre pon un timeout!"


def test_ej7_error_http_lanza_excepcion(monkeypatch):
    monkeypatch.setattr(pipeline.requests, "get", lambda *a, **k: RespuestaFalsa(500))
    with pytest.raises(pipeline.requests.HTTPError):
        pipeline.extraer(20.5, -100.8, "2025-01-01", "2025-01-31")

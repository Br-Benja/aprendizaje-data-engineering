import pandas as pd
import pipeline

def test_lluvia_minima_cuenta_como_lluvia():
    #PASO 1: Preparo los datos de entrada 
    base = pd.DataFrame({
        "fecha": pd.to_datetime(["2025-01-01", "2025-01-02"]),
        "temp_max": [26.0, 29.0],
        "temp_min": [8.0, 9.0],
        "precipitacion": [0.0, 0.1],
    })
    
    #PASO 2: llamo a la funcion que quiero probar
    df = pipeline.agregar_columnas(base, "Celaya")

    #PASO 3: Verificar el resultado esperado
    assert list(df["llovio"]) == [False, True]

def test_ciudad_en_todas_las_filas():
    #Paso 1: Preparar los datos de entrada
    base = pd.DataFrame({
            "fecha": pd.to_datetime(["2025-01-01", "2025-01-02","2025-01-03"]),
            "temp_max": [26.0, 29.0, 30.0],
            "temp_min": [8.0, 9.0, 10.0],
            "precipitacion": [0.0, 0.1, 0.2],
    })
    #Paso 2: Llamar a la funcion 
    df = pipeline.agregar_columnas(base,"Monterrey")

    #Paso 3: Verificar ciudad
    assert list(df["ciudad"]) == ["Monterrey", "Monterrey", "Monterrey"]
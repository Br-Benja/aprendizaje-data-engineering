# Lección 02 · Python para datos: mi primer pipeline ETL

En esta lección construyo un **pipeline ETL real**: descarga el clima diario de 2025 de Celaya, CDMX y Monterrey desde una API pública, lo limpia con **pandas**, lo guarda en **Parquet** y lo consulta con **SQL (DuckDB)**. Todo está validado con **tests automáticos (pytest)**.

```
 EXTRACT                     TRANSFORM                                LOAD
┌──────────────┐  JSON   ┌──────────────────────────────────┐   ┌─────────────────────────┐
│ API          │ ──────► │ a_dataframe → limpiar →          │──►│ datos/procesado/        │
│ Open-Meteo   │    │    │ agregar_columnas → resumen_mensual│   │   clima_diario.parquet  │──► SQL con DuckDB
└──────────────┘    │    └──────────────────────────────────┘   │   resumen_mensual.parquet│
                    ▼                                           └─────────────────────────┘
          datos/crudo/*.json   (copia sin tocar: permite reprocesar sin volver a llamar a la API)
```

## ▶️ Cómo trabajar

Desde la carpeta `fase-1-fundamentos/02-python`, con el entorno virtual activado:

```bash
pip install -r ../../requirements.txt      # instala pandas, pyarrow, requests, pytest (una sola vez)
py -m pytest -v                            # corre TODOS los tests (al inicio fallan los 15)
py -m pytest -v -k ej1                     # solo los del ejercicio 1
py pipeline.py                             # cuando todo pase: ¡corre el pipeline con datos reales!
```

1. Abre `pipeline.py`. Cada función con `TODO` es un ejercicio y su docstring explica qué debe hacer.
2. Borra el `raise NotImplementedError(...)` y escribe tu código.
3. Corre el test de ese ejercicio hasta que salga `PASSED` ✅.
4. Orden recomendado: **1 → 2 → 3 → 4 → 5 → 6 → 7**.
5. `soluciones/` solo después de lograrlo (o tras 20-30 min atorado).

> 💡 Para experimentar, abre una terminal de Python (`py`) y juega:
> `import pandas as pd; df = pd.DataFrame({"a": [1, 2, None]}); df.dropna()`

---

## 📚 Teoría

### 1. ¿Qué es ETL?
| Paso | Qué hace | En esta lección |
|---|---|---|
| **E**xtract | Saca datos de la fuente (API, base de datos, archivos) | `extraer()` con `requests` |
| **T**ransform | Limpia, valida, calcula, agrega | funciones con pandas |
| **L**oad | Guarda en el destino (data lake, warehouse) | `guardar_parquet()` |

En **ELT** (más moderno) primero se carga el dato crudo al warehouse y se transforma ahí con SQL. Es lo que hace **dbt** (Fase 2).

### 2. Consumir APIs con `requests` → *ej1, ej7*
```python
respuesta = requests.get(url, params={"ciudad": "Celaya"}, timeout=30)
respuesta.raise_for_status()   # lanza excepción si el código HTTP es 4xx o 5xx
datos = respuesta.json()       # convierte el JSON en dict/list de Python
```
- **`timeout` siempre.** Sin él, si la API se cuelga, tu pipeline se queda esperando para siempre.
- **`params`** arma el `?a=1&b=2` de la URL por ti (y escapa caracteres especiales).

### 3. pandas en 10 líneas → *ej2 a ej5*
```python
df = pd.DataFrame({"col": [1, 2]})        # crear desde dict de listas
df["nueva"] = df["col"] * 2                # columna calculada (vectorizada, ¡sin for!)
df[df["col"] > 1]                          # filtrar (como WHERE)
df.dropna(subset=["col"])                  # quitar nulos
df.fillna({"col": 0})                      # rellenar nulos
df.drop_duplicates(subset="id", keep="last")
df.sort_values("fecha").reset_index(drop=True)
df.groupby("ciudad", as_index=False).agg(total=("ventas", "sum"))   # como GROUP BY
```
Equivalencias con SQL:

| SQL | pandas |
|---|---|
| `WHERE` | `df[condicion]` |
| `GROUP BY` + `SUM` | `groupby(...).agg(...)` |
| `ORDER BY` | `sort_values(...)` |
| `JOIN` | `df.merge(otro, on="id", how="left")` |
| `ROW_NUMBER` para deduplicar | `drop_duplicates(keep="last")` |

⚠️ **No modifiques el DataFrame que recibes.** Una función que cambia su entrada provoca bugs difíciles de rastrear. Usa `df.copy()` o métodos que regresan un DataFrame nuevo. Los tests lo verifican.

### 4. ¿Por qué Parquet y no CSV? → *ej6*
| | CSV | Parquet |
|---|---|---|
| Formato | Texto, por filas | Binario, **columnar** |
| Tipos de datos | Se pierden (todo es texto) | Se conservan (fechas, enteros, booleanos) |
| Tamaño | Grande | 5-10× más pequeño (comprimido) |
| Leer 2 de 50 columnas | Lee todo el archivo | Lee solo esas 2 columnas |

Parquet es el **estándar en data lakes** (S3, GCS) y lo leen Spark, BigQuery, Snowflake, DuckDB…

### 5. Idempotencia → *ej6*
Un pipeline es **idempotente** si correrlo 1 o 10 veces produce el mismo resultado. Si falla a la mitad y lo vuelves a correr, no debe duplicar datos. Aquí lo logramos **sobrescribiendo** el archivo. Es una de las preguntas más comunes en entrevistas de Data Engineering.

### 6. Capas de datos: crudo → procesado
El pipeline guarda el JSON **tal como llegó** en `datos/crudo/` antes de transformarlo. Si mañana descubres un bug en `limpiar()`, puedes reprocesar sin volver a llamar a la API. En la industria a esto se le llama **arquitectura medallion**: bronze (crudo) → silver (limpio) → gold (agregado).

### 7. Tests con pytest
```python
def test_suma():
    assert sumar(2, 3) == 5
```
- Los tests son la **red de seguridad** de un pipeline: si cambias algo y rompes otra cosa, te enteras antes de producción.
- `monkeypatch` (ej7) reemplaza `requests.get` por una función falsa, así el test **no depende de internet**.
- `tmp_path` (ej6) da una carpeta temporal que pytest borra solo.

### 8. Logging en vez de `print`
`main()` usa `logging`: cada mensaje lleva fecha, hora y nivel (`INFO`, `WARNING`, `ERROR`). En producción esos logs se envían a herramientas de monitoreo. `print` no sirve para eso.

---

## 🎯 Reto extra (opcional)
- Agrega una 4ª ciudad a `CIUDADES` (por ejemplo tu ciudad natal; las coordenadas salen en Google Maps).
- Agrega la variable `wind_speed_10m_max` (viento) de punta a punta: parámetros → DataFrame → resumen.
- Escribe un test nuevo para tu cambio.

## 📝 Lo que aprendí
## 📝 Lo que aprendí

**Construí mi primer pipeline ETL completo:** descarga el clima de 2025 de tres ciudades
desde una API, limpia los datos con pandas, calcula columnas, genera un resumen mensual
y lo guarda en Parquet. Escribí las 7 funciones yo mismo y las validé con 16 tests de pytest.

- **pandas:** aprendí a trabajar con tablas en Python (DataFrames) y a hacer operaciones
  sobre columnas completas sin usar `for`. También descubrí que el `groupby` es el
  equivalente del `GROUP BY` de SQL.
- **Limpieza de datos:** aprendí a decidir cuándo eliminar un dato vacío y cuándo
  rellenarlo, y que es una decisión de negocio: rellenar una temperatura con 0 sería
  inventar un dato falso.
- **Idempotencia:** un pipeline es idempotente si correrlo 1 o 10 veces deja los datos
  exactamente igual, sin duplicados. Es lo mismo que logré antes en PostgreSQL con
  `ON CONFLICT DO UPDATE`.
- **Parquet vs CSV:** solo conocía CSV. Parquet es un formato binario, comprimido y
  columnar que conserva los tipos de datos; es el estándar en data lakes. CSV y JSON son
  texto, más fáciles de leer para una persona.
- **Tests:** aprendí que un test que pasa no garantiza que el código esté bien, y que
  después de cualquier cambio hay que correr todos los tests para detectar regresiones.

**Lo que más me costó:** aprender tantos conceptos nuevos a la vez y entender su
estructura, porque era la primera vez que los usaba. Lo que más me ayudó fue practicar
cada concepto con un ejemplo pequeño antes de usarlo en el pipeline.
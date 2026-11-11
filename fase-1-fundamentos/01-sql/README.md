# Lección 01 · SQL de cero a window functions

SQL es **la habilidad más evaluada** en entrevistas de Data Engineering. En esta lección practico sobre una tienda en línea ficticia usando **DuckDB**, una base de datos analítica que corre dentro de Python, sin instalar ningún servidor.

## 🗂️ Los datos

```
clientes (200)                 pedidos (2,000)                 detalle_pedidos (~3,800)
─────────────────              ─────────────────               ────────────────────────
cliente_id  PK  ◄──────────┐   pedido_id   PK  ◄────────────┐  pedido_id    FK
nombre                     └── cliente_id  FK               └─ producto_id  FK ──┐
ciudad (a veces NULL)          fecha_pedido (2024-2025)        cantidad          │
pais                           estado: completado /            precio_unitario   │
fecha_registro                         cancelado / pendiente                     │
                                                                                 │
productos (32)                                                                   │
─────────────────                                                                │
producto_id PK  ◄────────────────────────────────────────────────────────────────┘
nombre, categoria, precio (precio de lista)
```

> **Regla de negocio:** "ingresos" = `SUM(cantidad * precio_unitario)` **solo de pedidos con estado `'completado'`**.

## ▶️ Cómo trabajar

Desde la carpeta `fase-1-fundamentos/01-sql`, con el entorno virtual activado:

```bash
py generar_datos.py                                   # crea tienda.duckdb (una sola vez)
py explorar.py "SELECT * FROM pedidos LIMIT 5"        # explora los datos libremente
py revisar.py 1                                       # revisa tu ejercicio 1
py revisar.py                                         # revisa todos
```

1. Abre `ejercicios/ejNN.sql`, lee el enunciado y escribe tu consulta debajo.
2. Ejecuta `py revisar.py NN`. Te dice ✅ o ❌ y en qué fila está la diferencia.
3. **No abras `soluciones/` hasta tener ✅** (o después de intentarlo de verdad por 20 minutos). Compara tu solución con la oficial: a veces hay formas más limpias.

---

## 📚 Teoría

### 1. Orden lógico de ejecución (¡clave!)
Escribes `SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT`, pero la base de datos lo **ejecuta** en este orden:

```
FROM / JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```
Por eso no puedes usar en el `WHERE` un alias definido en el `SELECT`, pero sí en el `ORDER BY`.

### 2. Filtrar y ordenar → *ej01*
```sql
SELECT nombre, pais FROM clientes
WHERE pais IN ('Chile', 'Perú') AND ciudad IS NOT NULL   -- con NULL se usa IS, nunca =
ORDER BY nombre;
```

### 3. Agregar → *ej02, ej03*
`GROUP BY` colapsa filas en grupos; `COUNT`, `SUM`, `AVG`, `MIN` y `MAX` resumen cada grupo.
- `WHERE` filtra **filas antes** de agrupar.
- `HAVING` filtra **grupos después** de agrupar.

```sql
SELECT pais, COUNT(*) AS clientes
FROM clientes
GROUP BY pais
HAVING COUNT(*) > 30;
```

### 4. JOINs → *ej04, ej05*
| Tipo | Devuelve |
|---|---|
| `INNER JOIN` | Solo filas con coincidencia en ambas tablas |
| `LEFT JOIN` | Todas las de la izquierda; columnas de la derecha en `NULL` si no hay coincidencia |
| `FULL JOIN` | Todo de ambos lados |

Patrón clásico **"lo que NO tiene"**: `LEFT JOIN` + `WHERE derecha.id IS NULL` (o `NOT EXISTS`).

⚠️ **Trampa de entrevista:** un JOIN 1-a-muchos **multiplica filas**. Si unes `pedidos` con `detalle_pedidos`, cada pedido aparece una vez por producto. Por eso se usa `COUNT(DISTINCT pedido_id)`.

### 5. Fechas → *ej06*
```sql
DATE_TRUNC('month', fecha_pedido)   -- 2025-03-17 → 2025-03-01
EXTRACT(year FROM fecha_pedido)     -- 2025
fecha_pedido - DATE '2025-01-01'    -- diferencia en días (entero)
```
Para filtrar un año prefiere rangos (`>= '2025-01-01' AND < '2026-01-01'`) en vez de `EXTRACT(...) = 2025`: así se aprovechan índices y particiones.

### 6. CTEs (`WITH`) → *ej07*
Dividen una consulta compleja en pasos con nombre, como variables. En el trabajo real (y en **dbt**) casi todo se escribe así.
```sql
WITH ventas AS (
    SELECT ... ),
top AS (
    SELECT ... FROM ventas ... )
SELECT * FROM top;
```

### 7. Window functions → *ej08, ej09, ej10* ⭐
Calculan sobre un "ventana" de filas **sin colapsarlas** (a diferencia de `GROUP BY`).

```sql
funcion() OVER (PARTITION BY grupo ORDER BY columna)
```

| Función | Para qué |
|---|---|
| `ROW_NUMBER()` | 1, 2, 3… sin empates (top-N por grupo, **deduplicar**) |
| `RANK()` / `DENSE_RANK()` | Ranking con empates (1,1,3 / 1,1,2) |
| `LAG(col)` / `LEAD(col)` | Valor de la fila anterior/siguiente (crecimiento, diferencias) |
| `SUM(col) OVER (ORDER BY ...)` | Total acumulado (running total) |

Patrón **top-N por grupo** (muy común en entrevistas):
```sql
WITH r AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY precio DESC) AS rn
  FROM productos)
SELECT * FROM r WHERE rn <= 2;
```
💡 El mismo patrón con `rn = 1` sirve para **eliminar duplicados** quedándote con el registro más reciente. Lo usarás muchísimo en pipelines.

---

## 🎯 Después de los 10 ejercicios
- Resuelve 15 problemas *medium* de SQL en [DataLemur](https://datalemur.com) o [LeetCode](https://leetcode.com/studyplan/top-sql-50/).
- Marca esta lección como completada en el README principal, haz commit y súbelo a GitHub.

## 📝 Lo que aprendí
Aprendí a usar nuevas funciones que no conocía antes como el PARTITION BY, LAG(), ROW_NUMBER(), DATE_DIFF, ya que no tenía conocimiento de estas funciones y la verdad me sirvió para conocer un poco más sobre el manejo de las consultas de base de datos.


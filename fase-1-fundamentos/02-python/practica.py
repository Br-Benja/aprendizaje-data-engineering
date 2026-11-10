# Archivo de práctica: aquí escribo mis intentos de cada paso.
# Para ejecutarlo (desde la carpeta 02-python):  py practica.py

###### PASO 1 #####

#ciudad = "Monterrey"
#temperatura = 31.0 
#llovio = True

#print(ciudad)
#print(temperatura)
#print(llovio)

###### PASO 2  #####

#temp_max = 31.0
#temp_min = 20.0

#temp_promedio = (temp_max + temp_min)/2

#print(temp_promedio)
#print(f"En {ciudad} la temperatura promedio fue {temp_promedio} grados")

###### PASO 3 #####

#lluvia_monterrey = 5.5

#llovio = lluvia_monterrey > 0
#print(llovio)

#if lluvia_monterrey > 0.0:
#    print(f"Si llovio en {ciudad}, lleve paraguas ☔")

#else: 
#    print(f"No llovio en {ciudad} ☀️")


##### PASO 4 ##### 


#lluvias_celaya = [3.2, 3.6, 1.8]

#print(lluvias_celaya)
#print(lluvias_celaya[0])
#print(lluvias_celaya[2])
#print(len(lluvias_celaya))

#lluvias_celaya.append(0.5)
#print(lluvias_celaya)

#temperaturas_monterrey = [31.0,33.0,33.6]
#print(f"Posicion 1 del Arreglo {temperaturas_monterrey[0]}")
#print(f"Ultimo dato del arreglo {temperaturas_monterrey[len(temperaturas_monterrey)-1]}")
#print(f"Longitud del arreglo {len(temperaturas_monterrey)}")
#temperaturas_monterrey.append(30.2)
#print(f"Agregando valor al arreglo {temperaturas_monterrey}")



###### PASO 5: CICLO FOR  #####


#lluvias = [3.2, 0.0, 1.8]
#dias_con_lluvia = 0

#for lluvia in lluvias:
#    if lluvia > 0:
#        dias_con_lluvia = dias_con_lluvia + 1

#print(f"Llovió {dias_con_lluvia} días")

#temperaturas_monterrey = [31.0, 33.0, 33.6, 30.2, 34.1]
#dias_cont = 0

#for dias in temperaturas_monterrey:
#    if dias > 33:
#        dias_cont += 1

#print (f"Hubo un total de {dias_cont} con mas de 33 grados en {ciudad}")

###### PASO 6 DICCIONARIOS #####

#dia = {
#    "fecha": "2025-06-01",
#   "ciudad": "Celaya",
#    "temp_max": 27.6,
#   "lluvia": 3.2
#}

#print(dia["ciudad"])
#print(dia["lluvia"])

#dia["temp_min"] = 15.4
#print(dia)

#dia_monterrey = {
#    "fecha" : "2025-06-02",
#    "ciudad" : "Monterrey",
#    "temp_max" : 33.0,
#    "temp_min" : 21.4
#}

#print(dia_monterrey["temp_max"])

#dia_monterrey["temp_promedio"] = ((dia_monterrey["temp_max"] + dia_monterrey["temp_min"])/ 2)

#print(dia_monterrey["temp_promedio"])


##### Paso 7: Lista de diccionarios 📋📖 #####

#dias = [
#    {"fecha": "2025-06-01", "lluvia": 3.2},
#    {"fecha": "2025-06-02", "lluvia": 0.0},
#    {"fecha": "2025-06-03", "lluvia": 1.8},
#]

#print(dias[0])
#print(dias[0]["lluvia"])

#for dia in dias:
#    print(f"El {dia['fecha']} llovió {dia['lluvia']} mm")


#dias_monterrey = [
#    {"fecha": "2025-06-01", "temp_max": 31.0, "temp_min": 20.0},
#    {"fecha": "2025-06-02", "temp_max": 33.0, "temp_min": 21.4},
#    {"fecha": "2025-06-03", "temp_max": 33.6, "temp_min": 22.2},
#]

#print(dias_monterrey[-1]["temp_min"])

#for dia in dias_monterrey:
#    dia["temp_promedio"] = (dia["temp_max"] + dia["temp_min"]) /2
#    print(f"El {dia['fecha']} la máxima fue {dia['temp_max']} y la mínima {dia['temp_min']} con promedio de {dia['temp_promedio']}")


#for dias in dias_monterrey:
#    print(dias)


######## Paso 8: Funciones y return 🧩 ######### 

#def calcular_promedio(maxima, minima):
#    promedio = (maxima + minima) / 2
#    return promedio

#resultado = calcular_promedio(26.4, 8.1)
#print(resultado)

#print(calcular_promedio(31.0, 20.0))


#def crear_registro(fecha, lluvia):
#    return {
#        "fecha": fecha,
#        "lluvia": lluvia,
#        "llovio": lluvia > 0
#    }

#print(crear_registro("2025-06-01", 3.2))

#def es_dia_caluroso(temperatura):
#    return temperatura > 33

#print(es_dia_caluroso(34.1))
#print(es_dia_caluroso(31.0))

#def crear_dia(fecha, temp_max, temp_min): 
#    prom_dia = (temp_max+temp_min)/2
    

#    return {
#        "fecha" : fecha, 
#        "temp_max" : temp_max,
#        "temp_min" : temp_min,
#        "temp_promedio" : prom_dia 
#    }
    

#dia = crear_dia("2025-06-02", 33.0, 21.4)
#print(dia["temp_promedio"])

######## Paso 9: Tu primer ejercicio del pipeline real 🏗️ ###########

#DATOS = ["compra", "venta", "promedio"]

#def construir_parametros_cambio(origen, destino, fecha):
#    return {
#        "from": origen,
#        "to": destino,
#        "date": fecha,
#        "fields": ",".join(DATOS),
#        "format": "json"
#    }

#print(construir_parametros_cambio("USD", "MXN", "2025-06-01"))


##### PASO 10 PERDIRLE DATOS A LA API DESDE PYTHON ####### 

#import requests

#URL_POSTS = "https://jsonplaceholder.typicode.com/posts"

#def extraer_posts(usuario_id):
#    respuesta = requests.get(
#       URL_POSTS,
#        params={"userId": usuario_id},   # ← requests lo convierte en ?userId=1
#        timeout=30
#    )
#    respuesta.raise_for_status()
#    return respuesta.json()

#posts = extraer_posts(1)
#print(len(posts))
#print(posts[0]["title"])


############ PASO 11: PANDAS, TABLAS DENTRO DE PYTHON ############### 

#import pandas as pd

#datos = {
#   "fecha": ["2025-06-01", "2025-06-02", "2025-06-03"],
#    "temp_max": [27.6, 27.1, 27.1],
#    "temp_min": [15.4, 16.5, 15.5],
#}

#df = pd.DataFrame(datos)
#print(df)

#print(df["temp_max"])          # una columna
#print(len(df))                 # cuántas filas → 3
#print(df["temp_max"].mean())   # promedio de la columna → 27.27

#df["temp_promedio"] = (df["temp_max"] + df["temp_min"]) / 2   # columna nueva
#print(df)

#import pandas as pd
#datos = {
#    "fecha" : ["2025-06-01", "2025-06-02", "2025-06-03"],
#    "temp_max" :[31.0, 33.0, 33.6],
#    "lluvia" :[2.1, 0.0, 0.3]
#}

#df = pd.DataFrame(datos)

#print(df)

#total_lluvia = df["lluvia"].sum()
#print(total_lluvia)

#df["llovio"] = df["lluvia"] > 0

#print(df)


########### Paso 12: Convertir la respuesta de la API en tabla (ejercicio 2) 🏗️ #######


#import pandas as pd

#respuesta_ventas = {
#   "tienda": "Centro",
#    "data": {
#        "day": ["2025-03-01", "2025-03-02"],
#        "total_sales_mxn": [1500.0, 2300.5],
#        "items_sold": [12, 20],
#    }
#}

#def ventas_a_dataframe(respuesta):
#    data = respuesta["data"]
#    return pd.DataFrame({
#        "fecha": pd.to_datetime(data["day"]),
#        "ventas": data["total_sales_mxn"],
#        "piezas": data["items_sold"],
#    })

#df = ventas_a_dataframe(respuesta_ventas)
#print(df)
#print(df.dtypes)

########### Paso 13: Datos sucios, parte 1: valores vacíos 🧹 ###########

import pandas as pd

#ventas = pd.DataFrame({
#    "tienda": ["Centro", "Norte", "Sur", "Este"],
#    "ventas": [1500.0, None, 2300.5, 980.0],
#    "descuento": [100.0, 50.0, None, None],
#})
#print(ventas)
#print("") 

#sin_vacios = ventas.dropna(subset=["ventas"])
#print(sin_vacios)
#print("")

#rellenado = ventas.fillna({"descuento": 0.0})
#print(rellenado)
#print("")
#limpio = ventas.dropna(subset=["ventas"]).fillna({"descuento": 0.0})

#print(limpio)

#clima = pd.DataFrame({
#    "fecha": ["2025-06-01", "2025-06-02", "2025-06-03", "2025-06-04"],
#    "temp_max": [31.0, None, 33.6, 32.5],
#    "lluvia": [2.1, 0.0, None, 0.0],
#})

#print(clima)
#print("")

#sin_vacios = clima.dropna(subset={"temp_max"})
#print(sin_vacios)
#print("")

#relleno = clima.fillna({"lluvia" : 0.0})
#print(relleno)
#rint("")

#clima_limpio = clima.dropna(subset={"temp_max"}).fillna({"lluvia" : 0.0})
#print(clima_limpio)

####### Paso 14: Datos sucios, parte 2: duplicados y orden 🧹 #############

#ventas = pd.DataFrame({
#    "fecha": ["2025-03-03", "2025-03-01", "2025-03-02", "2025-03-02"],
#    "ventas": [800.0, 1500.0, 2000.0, 2300.5],
#})
#print(ventas)
#print("")

#limpio = (
#    ventas
#    .drop_duplicates(subset="fecha", keep="last") #si pongo en keep first se queda con el primero que llegue
#    .sort_values("fecha")
#    .reset_index(drop=True)
#)
#print(limpio)

############### Paso 15: Columnas calculadas (ejercicio 4) ➕ ##############

#def agregar_iva(df, tienda):
#    df = df.copy()                                   # 📋 fotocopia; el original queda intacto
#    df["con_iva"] = (df["precio"] * 1.16).round(2)   # columna calculada y redondeada
#    df["caro"] = df["precio"] > 1000                 # columna True/False
#    df["tienda"] = tienda                            # el MISMO valor para todas las filas
#    return df

#productos = pd.DataFrame({"precio": [500.0, 1200.0]})
#resultado = agregar_iva(productos, "Centro")
#print(resultado)
#print("")
#print(productos)      # ← el original sigue sin cambios

########### Paso 16: Agrupar datos, el GROUP BY de pandas 📊 #############

ventas = pd.DataFrame({
    "tienda": ["Centro", "Norte", "Centro", "Norte", "Centro"],
    "fecha": pd.to_datetime(["2025-03-01", "2025-03-01", "2025-03-15", "2025-04-02", "2025-04-10"]),
    "ventas": [1500.0, 900.0, 2300.5, 1100.0, 800.0],
    "con_descuento": [True, False, True, False, False],
})

#resumen = ventas.groupby("tienda", as_index=False).agg(
#    ventas_total=("ventas", "sum"),
#    venta_promedio=("ventas", "mean"),
#)
#print(resumen)

#resumen = (
#    ventas
#    .assign(mes=ventas["fecha"].dt.strftime("%Y-%m"))        # 🆕 crea la columna sin modificar el original
#    .groupby(["tienda", "mes"], as_index=False)
#    .agg(
#        ventas_total=("ventas", "sum"),
#        venta_promedio=("ventas", "mean"),
#        dias_con_descuento=("con_descuento", "sum"),         # 🧠 sumar True/False = contar los True
#    )
#    .round({"venta_promedio": 1})                            # 🆕 redondea solo esa columna
#    .sort_values(["tienda", "mes"])
#    .reset_index(drop=True)
#)
#print(resumen)

#################### Paso 17: Guardar los datos (ejercicio 6) 💾 #################3

#from pathlib import Path
#import pandas as pd

#def guardar_csv(df, ruta):
#    ruta = Path(ruta)
#    ruta.parent.mkdir(parents=True, exist_ok=True)
#    df.to_csv(ruta, index=False)

#ventas = pd.DataFrame({"tienda": ["Centro", "Norte"], "ventas": [1500.0, 900.0]})
#guardar_csv(ventas, "reportes/marzo/ventas.csv")

########## Paso 18: ¡Correr tu pipeline con datos reales! 🚀 #################


import pandas as pd
import pickle

def extraer_respuestas_correctas(archivo_respuestas_correctas):
    # Leer el archivo Excel de respuestas correctas
    df_correctas = pd.read_excel(archivo_respuestas_correctas, header=None)
    # Extraer las respuestas correctas de la segunda fila (índice 1) y columnas desde la sexta (índice 5) hasta la columna 65
    respuestas_correctas = df_correctas.iloc[1, 0:60].tolist()
    # Verificar que se tienen exactamente 60 respuestas correctas
    if len(respuestas_correctas) != 60:
        raise ValueError(f"Las respuestas correctas deben contener 60 elementos, pero tiene {len(respuestas_correctas)}")
    return respuestas_correctas

def comparar_respuestas(archivo_respuestas_alumnos, respuestas_correctas):
    # Leer el archivo Excel de respuestas de los alumnos
    df = pd.read_excel(archivo_respuestas_alumnos)
    # Crear un diccionario para almacenar los resultados de la comparación
    resultados_por_dni = {}
    # Iterar sobre las filas del DataFrame
    for index, row in df.iterrows():
        # Extraer el DNI (quinta columna), el nombre (cuarta columna)
        dni = row[3]
        nombre = row[2]
        correo = row[5]
        # Extraer las respuestas del alumno (de la columna 6 a la 65, índices 5 a 64)
        respuestas_alumno = row[6:66].tolist()
        # Verificar que se tienen exactamente 60 respuestas del alumno
        if len(respuestas_alumno) != 60:
            print(f"Advertencia: El alumno con DNI {dni} tiene {len(respuestas_alumno)} respuestas en lugar de 60. Se omitirá.")
            continue  # Saltar este alumno si no tiene 60 respuestas
        # Comparar las respuestas del alumno con las respuestas correctas
        comparacion = [1 if respuestas_alumno[i] == respuestas_correctas[i] else 0 for i in range(60)]
        # Almacenar el resultado en el diccionario
        resultados_por_dni[dni] = [correo, nombre] + comparacion
    return resultados_por_dni

def calcular_puntajes_por_area(resultados_por_dni):
    puntajes_por_area = {}
    for dni, datos in resultados_por_dni.items():
        correo = datos[0]
        nombre = datos[1]
        respuestas = datos[2:]
        # Dividir y sumar las respuestas por área
        puntaje_RV = sum(respuestas[:30]) * 2
        puntaje_RM = sum(respuestas[30:60]) * 2
        puntaje_NO = sum(respuestas[30:38]) * 2
        puntaje_EST = sum(respuestas[38:40]) * 2
        puntaje_ALG = sum(respuestas[40:50]) * 2
        puntaje_GEO = sum(respuestas[50:60]) * 2
        # Crear el diccionario para cada DNI
        puntajes_por_area[dni] = {
            "Correo": correo,
            "Nombre": nombre,
            "RV": puntaje_RV,
            "RM": puntaje_RM,
            "Números y Operaciones": puntaje_NO,
            "Álgebra": puntaje_ALG,
            "Geometría": puntaje_GEO,
            "Estadística": puntaje_EST
        }
    return puntajes_por_area

def guardar_en_pickle(puntajes_por_area, nombre_archivo_pickle):
    # Guardar el diccionario en un archivo pickle
    with open(nombre_archivo_pickle, 'wb') as f:
        pickle.dump(puntajes_por_area, f)
    print(f"Los datos han sido guardados en {nombre_archivo_pickle}")

# Ruta de los archivos Excel
archivo_respuestas_alumnos = 'D:\\REPORTE 2\\REPORTE_2_2\\SIMULACRO_29_11_2024.xlsx'
archivo_respuestas_correctas = 'D:\\REPORTE 2\\REPORTE_2_2\\RESPUESTAS_SIMULACRO_29_11.xlsx'
# Extraer las respuestas correctas
respuestas_correctas = extraer_respuestas_correctas(archivo_respuestas_correctas)
# Comparar las respuestas de los alumnos con las respuestas correctas
resultados_por_dni = comparar_respuestas(archivo_respuestas_alumnos, respuestas_correctas)
# Calcular los puntajes por área
puntajes_por_area = calcular_puntajes_por_area(resultados_por_dni)
# Guardar en Pickle
data2 = {str(key): value for key, value in puntajes_por_area.items()}
guardar_en_pickle(data2, "puntajes_2911.pkl")

# Cargar el archivo pickle
nombre_archivo_pickle = 'D:\REPORTE 2\REPORTE_2_2\puntajes_2911.pkl'
with open(nombre_archivo_pickle, 'rb') as f:
    puntajes_por_area_p = pickle.load(f)
print(puntajes_por_area_p)
import pickle
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.table import Table
from matplotlib.font_manager import FontManager
import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
import matplotlib.dates as mdates

def leer_datos_pickle(nombre_archivo_pickle):
    # Cargar el archivo pickle
    with open(nombre_archivo_pickle, 'rb') as f:
        puntajes_por_area = pickle.load(f)
    return puntajes_por_area

def calcular_porcentajes(puntajes_por_area):
    # Crear un nuevo diccionario para almacenar los porcentajes por área
    porcentajes_por_area = {}
    
    # Variables para almacenar la suma de porcentajes para cada área
    suma_RV = suma_RM = suma_NO = suma_ALG = suma_GEO = suma_EST = suma_TOT = suma_total_puntajes = 0
    total_personas = len(puntajes_por_area)
    
    for dni, datos in puntajes_por_area.items():
        nombre = datos["Nombre"]
        
        #Calcular puntaje_total
        puntaje_total = datos["RM"] + datos["RV"]
        # Calcular los porcentajes para cada área
        porcentaje_total = (datos["RM"] + datos["RV"])/120 * 100 #120 es el puntaje total posible
        porcentaje_RV = datos["RV"] / 60 * 100  # 60 es el puntaje total posible en RV
        porcentaje_RM = datos["RM"] / 60 * 100  # 60 es el puntaje total posible en RM
        porcentaje_NO = datos["Números y Operaciones"] / 16 * 100  # 16 es el puntaje total posible en N_O
        porcentaje_ALG = datos["Álgebra"] / 20 * 100  # 20 es el puntaje total posible en Álgebra
        porcentaje_GEO = datos["Geometría"]/ 20 * 100  # 20 es el puntaje total posible en Geometría
        porcentaje_EST = datos["Estadística"] / 4 * 100  # 4 es el puntaje total posible en Estadística
        # Sumar los porcentajes para calcular el promedio más adelante
        suma_total_puntajes += puntaje_total 
        suma_TOT += porcentaje_total
        suma_RV += porcentaje_RV
        suma_RM += porcentaje_RM
        suma_NO += porcentaje_NO
        suma_ALG += porcentaje_ALG
        suma_GEO += porcentaje_GEO
        suma_EST += porcentaje_EST
        # Almacenar los porcentajes en un diccionario bajo el DNI correspondiente
        porcentajes_por_area[dni] = {
            "Nombre": nombre,
            "Porcentaje TOT": porcentaje_total,
            "Porcentaje RV": porcentaje_RV,
            "Porcentaje RM": porcentaje_RM,
            "Porcentaje N_O": porcentaje_NO,
            "Porcentaje Álgebra": porcentaje_ALG,
            "Porcentaje Geometría": porcentaje_GEO,
            "Porcentaje Estadística": porcentaje_EST,
            "PUNTAJE TOTAL": puntaje_total
        }
    # Calcular el promedio de los porcentajes para cada área
    promedio_puntajes_total = suma_total_puntajes / total_personas
    promedio_TOT = suma_TOT / total_personas
    promedio_RV = suma_RV / total_personas
    promedio_RM = suma_RM / total_personas
    promedio_NO = suma_NO / total_personas
    promedio_ALG = suma_ALG / total_personas
    promedio_GEO = suma_GEO / total_personas
    promedio_EST = suma_EST / total_personas
    # Crear un diccionario con los promedios
    promedios = {
        "Promedio_TOT":promedio_TOT,
        "Promedio RV": promedio_RV,
        "Promedio RM": promedio_RM,
        "Promedio N_O": promedio_NO,
        "Promedio Álgebra": promedio_ALG,
        "Promedio Geometría": promedio_GEO,
        "Promedio Estadística": promedio_EST,
        "PROMEDIO TOTAL PUNTAJES": promedio_puntajes_total
    }
    return porcentajes_por_area, promedios

def generar_grafico_comparativo(directorio_salida, dni, porcentajes, promedios, dimension=(9, 9)):
    # Crear un gráfico con dimensiones personalizadas
    fig, ax = plt.subplots(figsize=dimension)
    # Etiquetas de las áreas
    etiquetas = ['RV', 'Aritmética', 'Álgebra', 'Geometría', 'Estadística']
    # Valores personales
    valores_personal = [
        porcentajes[dni]["Porcentaje RV"],
        porcentajes[dni]["Porcentaje N_O"], 
        porcentajes[dni]["Porcentaje Álgebra"], 
        porcentajes[dni]["Porcentaje Geometría"], 
        porcentajes[dni]["Porcentaje Estadística"], 
    ]
    # Valores grupales (promedios)
    valores_grupal = [
        promedios["Promedio RV"],
        promedios["Promedio N_O"], 
        promedios["Promedio Álgebra"], 
        promedios["Promedio Geometría"], 
        promedios["Promedio Estadística"], 
    ]
    # Definir la posición de las barras
    x = np.arange(len(etiquetas))
    ancho = 0.40  # El ancho de las barras
    # Crear las barras
    barras_personal = ax.bar(x - ancho/2, valores_personal, ancho, label='Personal', color='#015989')
    barras_grupal = ax.bar(x + ancho/2, valores_grupal, ancho, label='Grupal', color='#e64f41')
    # Añadir etiquetas, título y leyenda
    #ax.set_title('PORCENTAJE DE ACIERTOS')
    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas)
    ax.legend(fontsize = 17)
    # Añadir el valor porcentual dentro o encima de las barras
    for barra in barras_personal:
        yval = barra.get_height()
        if yval > 90:
            ax.text(barra.get_x() + barra.get_width()/2, yval / 2, f"{yval:.2f}%", ha='center', va='center', color='white')
        else:
            ax.text(barra.get_x() + barra.get_width()/2, yval + 1, f"{yval:.2f}%", ha='center', va='bottom')
    for barra in barras_grupal:
        yval = barra.get_height()
        if yval > 90:
            ax.text(barra.get_x() + barra.get_width()/2, yval / 2, f"{yval:.2f}%", ha='center', va='center', color='white')
        else:
            ax.text(barra.get_x() + barra.get_width()/2, yval + 1, f"{yval:.2f}%", ha='center', va='bottom')
    plt.ylim(0, 100)
    plt.tight_layout()
    # Asegurarse de que el directorio existe y solo construir la ruta una vez
    #directorio_salida = os.path.join('graficos_reportes_15_09')
    os.makedirs(directorio_salida, exist_ok=True)  # Crear el directorio si no existe
    # Guardar el gráfico como archivo PNG
    ruta_grafico = os.path.join(directorio_salida, f"grafico_comparativo_{dni}.png")
    plt.savefig(ruta_grafico, transparent=True)
    plt.close()
    return ruta_grafico

def crear_grafico_aciertos_por_curso(directorio_salida, datos_persona, dni, dimension=(6, 8), espaciado_vertical=0.8):
    nombre = datos_persona[dni]["Nombre"]
    # Configurar los datos de cada área
    etiquetas = [
        f"E y P ({datos_persona[dni]['Estadística'] // 2} de 2)",
        f"Geometría ({datos_persona[dni]['Geometría'] // 2} de 10)",
        f"Álgebra ({datos_persona[dni]['Álgebra'] // 2} de 10)",
        f"Aritmética ({datos_persona[dni]['Números y Operaciones'] // 2} de 8)",
        f"RV ({datos_persona[dni]['RV'] // 2} de 30)"
    ]
    valores = [
        datos_persona[dni]['Estadística'] / 4 * 100,
        datos_persona[dni]['Geometría']/ 20 * 100,
        datos_persona[dni]['Álgebra'] / 20 * 100,
        datos_persona[dni]['Números y Operaciones'] / 16 * 100,
        datos_persona[dni]['RV'] / 60 * 100
    ]
    # Configurar el gráfico
    fig, ax = plt.subplots(figsize=dimension)
    # Colores personalizados
    color_azul = '#015989'
    color_amarillo = '#f9b52b'
    # Posiciones de las barras
    y_positions = np.arange(len(etiquetas)) * espaciado_vertical
    # Dibujar barras horizontales con control del espaciado vertical
    for i, (label, valor) in enumerate(zip(etiquetas, valores)):
        ax.barh(y_positions[i], 100, color=color_amarillo, height=0.4)  # Fondo amarillo
        ax.barh(y_positions[i], valor, color=color_azul, height=0.4)  # Progreso en azul
        ax.text(5, y_positions[i], label, va='center', ha='left', fontsize=18, fontweight = 'bold',color='white')  # Posicionar la etiqueta al principio
    # Configurar las etiquetas y el formato
    ax.set_yticks([])  # Ocultar el eje y
    ax.set_xlim(0, 100)
    ax.set_xticks([])
    #Ajustar los límites del eje y para acomodar el espaciado
    ax.set_ylim(-espaciado_vertical, y_positions[-1] + espaciado_vertical)
    # Eliminar los bordes del gráfico
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.tight_layout()
    # Asegurarse de que el directorio existe y solo construir la ruta una vez
    #directorio_salida = os.path.join('graficos_reportes_15_09')
    os.makedirs(directorio_salida, exist_ok=True)  # Crear el directorio si no existe
    # Guardar el gráfico como archivo PNG con el DNI en el nombre del archivo
    ruta_grafico = os.path.join(directorio_salida, f"grafico_aciertos_por_curso_{dni}.png")
    plt.savefig(ruta_grafico, bbox_inches='tight', transparent=True)
    plt.close()
    return ruta_grafico

def HISTORICO_PORCENTAJES(directorio_salida, dni, *args, dimension=(23, 7)):
    #Inicializar para almacenar las fechas, puntajes grupales e individuales
    fechas = []
    porcentajes_individual = []
    porcentajes_grupal = []

    # Extraer las fechas y porcentajes de los argumentos
    for i in range(0, len(args), 3):
        fecha = args[i]
        porcentajes_inv = args[i+1]
        porcentajes_prom = args[i+2]
        # Guardar las fechas
        fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
        fechas.append(fecha_dt)
        # Verificar si el DNI existe en los porcentajes individuales
        if dni in porcentajes_inv:
            porcentajes_individual.append(porcentajes_inv[dni]["PUNTAJE TOTAL"])  # O cualquier otra área (RV, RM, etc.)
        else:
            porcentajes_individual.append(np.nan)  # Dejar un vacío si el DNI no está presente
        # Usar los promedios generales para los porcentajes grupales
        porcentajes_grupal.append(porcentajes_prom["PROMEDIO TOTAL PUNTAJES"])  # O cualquier otra área (RV, RM, etc.)

    # Crear el gráfico
    plt.figure(figsize=dimension)
    # Añadir una línea horizontal roja y punteada en el valor 60
    plt.axhline(y=70, color='#e64f41', linestyle='--', linewidth=3, label='Línea de referencia (70 puntos)')
    # Graficar los puntos individuales y grupales
    plt.plot(fechas, porcentajes_individual, marker='o', color='#f9b52b', label='Individual', linewidth=2.5)
    plt.plot(fechas, porcentajes_grupal, marker='o', color='#015989', label='Grupo', linewidth=2.5)
    # Añadir etiquetas, título y leyenda
    plt.xlabel('Fecha', fontsize = 24)
    plt.ylabel('Puntaje', fontsize = 24)
    #plt.title(f'Evolución de Notas Respecto al Grupo')
    plt.ylim(0, 120)
    plt.legend(loc='best', fontsize = 20)
    # Ajustar los límites del eje x para agregar margen en los extremos
    margen = timedelta(days = 2)  # Puedes ajustar este valor
    plt.xlim(fechas[0] - margen, fechas[-1] + margen)
    # Formatear el eje de fechas
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

    #COLOCAR LOS DIAS DE LAS FECHAS
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(bymonthday = (18, 20, 22, 25, 27, 29), interval = 1))
    plt.gca().tick_params(axis = 'x', labelsize = 18)
    y_ticks = plt.gca().get_yticks()
    new_y_ticks = list(y_ticks) + [70]
    plt.yticks(new_y_ticks)
    plt.gca().tick_params(axis = 'y', labelsize = 18)
    #COLOCAR LOS DIAS DE LAS FECHAS

    #plt.gcf().autofmt_xdate()  # Rotar las fechas si es necesario
    # Añadir etiquetas de porcentaje sobre los puntos
    for i, (ind, grp) in enumerate(zip(porcentajes_individual, porcentajes_grupal)):
        ver = -5
        if not np.isnan(ind):  # Solo etiquetar si hay datos
            if ind>grp:
                ver = 4
            else:
                ver = -4
            plt.text(fechas[i], ind + ver, f'{ind:.2f}', ha='center', va='center', color='#f9b52b', fontsize = 22, fontweight='bold')
        plt.text(fechas[i], grp - ver, f'{grp:.2f}', ha='center', va='center', color='#015989', fontsize = 22, fontweight='bold')
    plt.tight_layout()
    # Asegurarse de que el directorio existe y solo construir la ruta una vez
    #directorio_salida = os.path.join('graficos_reportes_15_09')
    os.makedirs(directorio_salida, exist_ok=True)  # Crear el directorio si no existe
    # Guardar el gráfico
    ruta_grafico = os.path.join(directorio_salida, f"historico_porcentajes_{dni}.png")
    plt.savefig(ruta_grafico, transparent=True)
    plt.close()
    return ruta_grafico

def generar_recomendaciones(directorio_salida, dni, porcentajes_por_area):
    # Definir los mensajes según los rangos de porcentaje
    def obtener_mensaje(porcentaje):
        if porcentaje <= 25:
            return "Vamos futur@ becari@, debes repasar con urgencia este curso para lograr la meta"
        elif 25 < porcentaje <= 50:
            return "Vamos tienes que repasar mas este curso. ¡Tu puedes!"
        elif 50 < porcentaje <= 75:
            return "Bien, respasa un poco mas este curso y estarás listo"   
        else:
            return "¡Muy bien! sigue asi en este curso"
    
    porcentajes = {
        "Razonamiento Verbal": porcentajes_por_area[dni]["Porcentaje RV"],
        "Aritmética": porcentajes_por_area[dni]["Porcentaje N_O"],
        "Álgebra": porcentajes_por_area[dni]["Porcentaje Álgebra"],
        "Geometría": porcentajes_por_area[dni]["Porcentaje Geometría"],
        "Estadística": porcentajes_por_area[dni]["Porcentaje Estadística"]
    }   
    # Crear el gráfico de recomendaciones
    fig, ax = plt.subplots(figsize=(20, 5.5))
    ax.set_axis_off()
    # Ajustar el fondo dinámicamente según el texto más largo
    recomendaciones = [f"• {area}: {obtener_mensaje(porcentaje)}" for area, porcentaje in porcentajes.items()]
    # Título y recomendaciones
    ax.text(0.05, 0.9, "RECOMENDACIONES:", fontsize=18, fontweight='bold', color='white', transform=ax.transAxes)
    rect = patches.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color='#e64f41')
    ax.add_patch(rect)
    # Espaciado dinámico para asegurarse de que todas las recomendaciones se alinean correctamente
    spacing = 0.65/len(recomendaciones)
    for i, recomendacion in enumerate(recomendaciones):
        ax.text(0.05, 0.7 - i * spacing, recomendacion, fontsize=16, fontweight='bold', color='white', transform=ax.transAxes)
    # Asegurarse de que el directorio existe y solo construir la ruta una vez
    #directorio_salida = os.path.join('graficos_reportes_15_09')
    os.makedirs(directorio_salida, exist_ok=True)  # Crear el directorio si no existe
    # Guardar la imagen
    ruta_grafico = os.path.join(directorio_salida, f"recomendaciones_{dni}.png")
    plt.savefig(ruta_grafico, bbox_inches='tight', transparent=True)
    plt.close()
    return ruta_grafico

def generar_posiciones_por_puntaje(puntajes_por_area):
    # Crear un diccionario para almacenar los puntajes totales por estudiante
    puntajes_totales = {}
    
    for dni, datos in puntajes_por_area.items():
        nombre = datos['Nombre']
        puntaje_total = datos['RV'] + datos['RM']
        puntajes_totales[dni] = {
            'Nombre': nombre,
            'Puntaje Total': puntaje_total
        }
    # Ordenar a los estudiantes por su puntaje total de mayor a menor
    ranking = sorted(puntajes_totales.items(), key=lambda x: x[1]['Puntaje Total'], reverse=True)
    # Asignar las posiciones en el ranking
    for idx, (dni, datos) in enumerate(ranking, 1):
        puntajes_totales[dni]['Posicion'] = idx
    return puntajes_totales

def generar_cuadro_posicion(directorio_salida, dni, puntajes_totales):
    # Obtener el total de alumnos automáticamente
    total_estudiantes = len(puntajes_totales)
    # Crear el cuadro de posición para cada estudiante
    nombre = puntajes_totales[dni]['Nombre']
    posicion = puntajes_totales[dni]['Posicion']
    puntaje = puntajes_totales[dni]['Puntaje Total'] 
    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(100, 5))
    ax.set_axis_off()
    tam_letra = 90
    # Texto del cuadro
    #print(len("ALUMNO:"))
    #print(len(nombre))
    tam_nombre = len(nombre)
    tam_posi = len(f"  {posicion} de {total_estudiantes}")
    ax.text(0.05, 0.55, "ALUMNO:", fontsize=tam_letra, fontweight='bold', color='black', transform=ax.transAxes)
    ax.text(0.14, 0.55, nombre, fontsize=tam_letra, color='black', transform=ax.transAxes)
    ax.text(0.14 + tam_nombre * 0.0086, 0.55, "   POSICIÓN RELATIVA:          ", fontsize=tam_letra, fontweight='bold', color='black', transform=ax.transAxes)
    ax.text(0.14 + tam_nombre * 0.0086 + 0.16, 0.55, f"         {posicion} de {total_estudiantes}", fontsize=tam_letra, color='black', transform=ax.transAxes)
    ax.text(0.14 + tam_nombre * 0.0086 + 0.16 + tam_posi * 0.012, 0.55, "  PUNTAJE TOTAL:", fontsize=tam_letra, fontweight='bold', color='black', transform=ax.transAxes)
    ax.text(0.14 + tam_nombre * 0.0086 + 0.16 + tam_posi * 0.012 + 0.15, 0.55, f"  {puntaje} de 120", fontsize=tam_letra, color='black', transform=ax.transAxes)
    # Asegurarse de que el directorio existe y solo construir la ruta una vez
    #directorio_salida = os.path.join('graficos_reportes_15_09')
    os.makedirs(directorio_salida, exist_ok=True)  # Crear el directorio si no existe
    # Guardar la imagen
    ruta_grafico = os.path.join(directorio_salida, f"posicion_{dni}.png")
    plt.savefig(ruta_grafico, bbox_inches='tight', transparent=True)
    plt.close()
    #print(f"Posición generada para {nombre}: {ruta_grafico}")
    return ruta_grafico

def extraer_respuestas_correctas_alumnos(archivo_respuestas_correctas, archivo_respuestas_alumnos):
    # Leer el archivo Excel de respuestas correctas
    df_correctas = pd.read_excel(archivo_respuestas_correctas, header=None)
    # Extraer las respuestas correctas de la segunda fila (índice 1) y columnas desde la sexta (índice 5) hasta la columna 65
    respuestas_correctas = df_correctas.iloc[1, 0:60].tolist()
    # Verificar que se tienen exactamente 60 respuestas correctas
    if len(respuestas_correctas) != 60:
        raise ValueError(f"Las respuestas correctas deben contener 60 elementos, pero tiene {len(respuestas_correctas)}")
    # Leer el archivo Excel de respuestas de los alumnos
    df = pd.read_excel(archivo_respuestas_alumnos)
    # Crear un diccionario para almacenar los resultados de cada alumno
    claves_alum = {}
    # Iterar sobre las filas del DataFrame
    for index, row in df.iterrows():
        # Extraer el DNI (quinta columna), el nombre (cuarta columna)
        dni = row[3]
        nombre = row[2]     
        # Extraer las respuestas del alumno (de la columna 6 a la 65, índices 5 a 64)
        respuestas_alumno = row[6:66].tolist()
        # Verificar que se tienen exactamente 60 respuestas del alumno
        if len(respuestas_alumno) != 60:
            print(f"Advertencia: El alumno con DNI {dni} tiene {len(respuestas_alumno)} respuestas en lugar de 60. Se omitirá.")
            continue  # Saltar este alumno si no tiene 60 respuestas
   
    # Almacenar el resultado en el diccionario
        claves_alum[str(dni)] = [nombre] + respuestas_alumno

    return respuestas_correctas, claves_alum

def generar_tabla_respuestas_comparativa(directorio_salida, dni, archivo_respuestas_correctas, archivo_respuestas_alumnos):
    respuestas_correctas, respuestas_alumno_1 = extraer_respuestas_correctas_alumnos(archivo_respuestas_correctas, archivo_respuestas_alumnos)
    respuestas_alumno = respuestas_alumno_1[dni][1:61]
    fig, ax = plt.subplots(figsize=(25, 25))
    ax.set_axis_off()
    # Crear la tabla
    tabla = Table(ax, bbox=[0, 0, 1, 1])
    # Encabezados
    columnas = ['#', 'Tú', 'Clave', '#', 'Tú', 'Clave', '#', 'Tú', 'Clave', '#', 'Tú', 'Clave']
    cell_text = []
    respuestas_correctas_mod = []
    # Organizar los datos en columnas de 15 preguntas cada una (total 60 preguntas)
    for i in range(0, 15):
        for j in range(4):
            if i + j < 60:
                cell_text.append([str(i + j*15 + 1), respuestas_alumno[i + j*15], respuestas_correctas[i + j*15]])
                respuestas_correctas_mod.append(respuestas_correctas[i + j*15])

    # Separar en grupos de 4 columnas
    nrows =  len(cell_text) // 4
    ncols = 12  # 4 bloques de [# Respuesta Clave]
    # Agregar celdas de encabezado
    for i in range(ncols):
        cell = tabla.add_cell(0, i, 0.075, 0.05, text=columnas[i], loc='center', facecolor='#f9b52b')
        #cell.get_text().set_color('white')
        cell.get_text().set_fontsize(20)
        cell.get_text().set_fontweight('bold')

    # Añadir los datos de las respuestas por columnas
    for i in range(nrows):
        text_ant = "qqwewqrwqrq"
        for j in range(ncols):

            if pd.isna(cell_text[i * 4 + (j // 3)][j % 3]):
                text = "--"
            else:
                text = cell_text[i * 4 + (j // 3)][j % 3]

            if j % 3 == 0:
                cell = tabla.add_cell(i + 1, j, 0.075, 0.05, text=text, loc='center',
                           facecolor='#015989')
                cell.get_text().set_fontsize(20)
                cell.get_text().set_color('white')
                cell.get_text().set_fontweight('bold')

            elif j % 3 == 1:
                cell = tabla.add_cell(i + 1, j, 0.075, 0.05, text=text, loc='center',
                           facecolor='white' if text == respuestas_correctas_mod[i * 4 + (j // 3)] else '#e64f41')
                cell.get_text().set_fontsize(20)
                cell.get_text().set_fontweight('bold')
            else:
                cell = tabla.add_cell(i + 1, j, 0.075, 0.05, text=text, loc='center',
                           facecolor='white' if text_ant == respuestas_correctas_mod[i * 4 + (j // 3)] else '#e64f41')
                cell.get_text().set_fontsize(20)
                cell.get_text().set_fontweight('bold')
            text_ant = text


    ax.add_table(tabla)
    # Asegurarse de que el directorio existe y solo construir la ruta una vez
    #directorio_salida = os.path.join('graficos_reportes_15_09')
    os.makedirs(directorio_salida, exist_ok=True)  # Crear el directorio si no existe
    # Guardar el gráfico
    ruta_imagen = os.path.join(directorio_salida, f"respuestas_comparativa_{dni}.png")
    plt.savefig(ruta_imagen, transparent=True)
    plt.close()
    return ruta_imagen
import os
import fitz  # PyMuPDF
from GRAFICAR_CON_DATOS import (generar_grafico_comparativo, crear_grafico_aciertos_por_curso, 
                                HISTORICO_PORCENTAJES, generar_recomendaciones, generar_cuadro_posicion,
                                generar_tabla_respuestas_comparativa, leer_datos_pickle, generar_posiciones_por_puntaje, calcular_porcentajes)
from GUARDAR_PUNTAJES import (guardar_en_pickle)
import pandas as pd

def crear_carpeta(nombre_carpeta):
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)

def generar_graficas_y_reportes(directorio_salida, dni,puntajes_por_area, dimension, espaciado_vertical, archivo_respuestas, archivo_alumnos, puntajes_totales, *args):
    #carpeta_graficas = "graficos_reportes_15_09"
    #crear_carpeta(carpeta_graficas)
    porcentajes_por_area = args[-2]
    promedios = args[-1]

    #1. generar_grafico_comparativo
    ruta_grafico_comparativo = generar_grafico_comparativo(directorio_salida, dni, porcentajes_por_area, promedios, dimension)
    #2. crear_grafico_aciertos_por_curso
    ruta_grafico_aciertos = crear_grafico_aciertos_por_curso(directorio_salida, puntajes_por_area, dni, dimension,espaciado_vertical)
    #3. HISTORICO_PORCENTAJES
    ruta_historico = HISTORICO_PORCENTAJES(directorio_salida, dni, *args)
    #4. generar_recomendaciones
    ruta_recomendaciones = generar_recomendaciones(directorio_salida, dni, porcentajes_por_area)
    #5. generar_cuadro_posicion
    ruta_posicion = generar_cuadro_posicion(directorio_salida, dni, puntajes_totales)
    #6. generar_tabla_respuestas_comparativa
    ruta_tabla = generar_tabla_respuestas_comparativa(directorio_salida, dni, archivo_respuestas, archivo_alumnos)
    
    return {
        "pos#_REL_AL": ruta_posicion,
        "num#_acier_TODO": ruta_grafico_aciertos,
        "por%_acier_COMP": ruta_grafico_comparativo,
        "desem%_TODOS": ruta_historico,
        "reco#_da": ruta_recomendaciones,
        "TABLA#_RES#": ruta_tabla
    }

def insertar_graficas_en_posiciones(directorio_salida_reportes, pdf_plantilla, ruta_salida, graficas_generadas):
    doc = fitz.open(pdf_plantilla)

    pagina_1 = 0  # Las páginas en fitz empiezan en 0
    # Obtener la página del documento PDF
    page_1 = doc[pagina_1]

    #Insertamos la primera imagen
    coordenadas_1 = (-15, 155.8, 580, 187.8)
    ruta_imagen_1 = graficas_generadas["pos#_REL_AL"]
    # Insertar la imagen en el rectángulo especificado
    rect_1 = fitz.Rect(*coordenadas_1)
    page_1.insert_image(rect_1, filename=ruta_imagen_1)
    
    #Insertamos la segunda imagen
    coordenadas_2 = (22, 198, 212, 466)
    ruta_imagen_2 = graficas_generadas["num#_acier_TODO"]
    # Insertar la imagen en el rectángulo especificado
    rect_2 = fitz.Rect(*coordenadas_2)
    page_1.insert_image(rect_2, filename=ruta_imagen_2)
    
    #Insertamos la tercera imagen
    coordenadas_3 = (216, 205, 582, 445)
    ruta_imagen_3 = graficas_generadas["por%_acier_COMP"]
    # Insertar la imagen en el rectángulo especificado
    rect_3 = fitz.Rect(*coordenadas_3)
    page_1.insert_image(rect_3, filename=ruta_imagen_3)
    
    #Insertamos la cuarta imagen
    coordenadas_4 = (20, 460, 575, 660)
    ruta_imagen_4 = graficas_generadas["desem%_TODOS"]
    # Insertar la imagen en el rectángulo especificado
    rect_4 = fitz.Rect(*coordenadas_4)
    page_1.insert_image(rect_4, filename=ruta_imagen_4)
    
    #Insertamos la quinta imagen
    coordenadas_5 = (68, 600, 538, 830)
    ruta_imagen_5 = graficas_generadas["reco#_da"]
    # Insertar la imagen en el rectángulo especificado
    rect_5 = fitz.Rect(*coordenadas_5)
    page_1.insert_image(rect_5, filename=ruta_imagen_5)
    
    #Insertamos la sexta imagen
    pagina_6 = 1
    page_6 = doc[pagina_6]
    coordenadas_6 = (-35, 110, 620, 870)
    ruta_imagen_6 = graficas_generadas["TABLA#_RES#"]
    # Insertar la imagen en el rectángulo especificado
    rect_6 = fitz.Rect(*coordenadas_6)
    page_6.insert_image(rect_6, filename=ruta_imagen_6)

    # Asegurarse de que el directorio existe y solo construir la ruta una vez
    #directorio_salida = os.path.join('reportes_15_09')
    os.makedirs(directorio_salida_reportes, exist_ok=True)  # Crear el directorio si no existe
    # Guardar el PDF actualizado
    ruta_completa = os.path.join(directorio_salida_reportes, ruta_salida)
    doc.save(ruta_completa)
    doc.close()
    print(f"PDF guardado en {ruta_salida}")
    return ruta_completa

def generar_reporte_pdf(directorio_salida_reportes, directorio_salida, dni, plantilla_pdf, dimension,espaciado_vertical, puntajes_por_area, archivo_respuestas, archivo_alumnos, puntajes_totales, *args):
    
    # Generar las gráficas
    graficas_generadas = generar_graficas_y_reportes(directorio_salida, dni,puntajes_por_area, dimension, espaciado_vertical, archivo_respuestas, archivo_alumnos, puntajes_totales, *args)
    # Insertar las gráficas en la plantilla del PDF
    ruta_pdf_salida = f"reporte_{puntajes_por_area[dni]['Nombre']}.pdf"
    ruta_completa = insertar_graficas_en_posiciones(directorio_salida_reportes, plantilla_pdf, ruta_pdf_salida, graficas_generadas)
    return ruta_completa, puntajes_por_area[dni]['Nombre'], puntajes_por_area[dni]['Correo']

# Nombre de los archivos pickle
#nombre_archivo_pickle1509 = 'puntajes_1509.pkl'
#nombre_archivo_pickle0709 = 'puntajes_0709.pkl'
#nombre_archivo_pickle2209 = 'puntajes_2209.pkl'
#nombre_archivo_pickle2809 = 'puntajes_2809.pkl'
#nombre_archivo_pickle0510 = 'puntajes_0510.pkl'
#nombre_archivo_pickle1210 = 'puntajes_1210.pkl'
#nombre_archivo_pickle1910 = 'puntajes_1910.pkl'
#nombre_archivo_pickle2610 = 'puntajes_2610.pkl'
#nombre_archivo_pickle0211 = 'puntajes_0211.pkl'
#nombre_archivo_pickle0911 = 'puntajes_0911.pkl'
nombre_archivo_pickle1811 = 'puntajes_1811.pkl'
nombre_archivo_pickle2011 = 'puntajes_2011.pkl'
nombre_archivo_pickle2211 = 'puntajes_2211.pkl'
nombre_archivo_pickle2511 = 'puntajes_2511.pkl'
nombre_archivo_pickle2711 = 'puntajes_2711.pkl'
nombre_archivo_pickle2911 = 'puntajes_2911.pkl'
# Uso del código:
espaciado_vertical = 0.6
dimension = (8, 8)


#EVALUACION 07/09/2024
#puntajes_por_area_0709 = leer_datos_pickle(nombre_archivo_pickle0709)
#porcentajes_por_area0709, promedios0709 = calcular_porcentajes(puntajes_por_area_0709)
#EVALUACION 15/09/2024
#puntajes_por_area_1509 = leer_datos_pickle(nombre_archivo_pickle1509)
#porcentajes_por_area_1509, promedios1509 = calcular_porcentajes(puntajes_por_area_1509)
#puntajes_totales_1509 = generar_posiciones_por_puntaje(puntajes_por_area_1509)
#EVALUACION 22/09/2024
#puntajes_por_area_2209 = leer_datos_pickle(nombre_archivo_pickle2209)
#porcentajes_por_area_2209, promedios2209 = calcular_porcentajes(puntajes_por_area_2209)
#puntajes_totales_2209 = generar_posiciones_por_puntaje(puntajes_por_area_2209)
#EVALUACION 28/09/2024
#puntajes_por_area_2809 = leer_datos_pickle(nombre_archivo_pickle2809)
#porcentajes_por_area_2809, promedios2809 = calcular_porcentajes(puntajes_por_area_2809)
#puntajes_totales_2809 = generar_posiciones_por_puntaje(puntajes_por_area_2809)
#EVALUACION 05/10/2024
#puntajes_por_area_0510 = leer_datos_pickle(nombre_archivo_pickle0510)
#porcentajes_por_area_0510, promedios0510 = calcular_porcentajes(puntajes_por_area_0510)
#puntajes_totales_0510 = generar_posiciones_por_puntaje(puntajes_por_area_0510)
#EVALUACION 12/10/2024
#puntajes_por_area_1210 = leer_datos_pickle(nombre_archivo_pickle1210)
#porcentajes_por_area_1210, promedios1210 = calcular_porcentajes(puntajes_por_area_1210)
#puntajes_totales_1210 = generar_posiciones_por_puntaje(puntajes_por_area_1210)
#EVALUACION 19/10/2024
#puntajes_por_area_1910 = leer_datos_pickle(nombre_archivo_pickle1910)
#porcentajes_por_area_1910, promedios1910 = calcular_porcentajes(puntajes_por_area_1910)
#puntajes_totales_1910 = generar_posiciones_por_puntaje(puntajes_por_area_1910)
#EVALUACION 26/10/2024
#puntajes_por_area_2610 = leer_datos_pickle(nombre_archivo_pickle2610)
#porcentajes_por_area_2610, promedios2610 = calcular_porcentajes(puntajes_por_area_2610)
#puntajes_totales_2610 = generar_posiciones_por_puntaje(puntajes_por_area_2610)
#EVALUACION 02/11/2024
#puntajes_por_area_0211 = leer_datos_pickle(nombre_archivo_pickle0211)
#porcentajes_por_area_0211, promedios0211 = calcular_porcentajes(puntajes_por_area_0211)
#puntajes_totales_0211 = generar_posiciones_por_puntaje(puntajes_por_area_0211)



#EVALUACION 18/11/2024
puntajes_por_area_1811 = leer_datos_pickle(nombre_archivo_pickle1811)
porcentajes_por_area_1811, promedios1811 = calcular_porcentajes(puntajes_por_area_1811)
puntajes_totales_1811 = generar_posiciones_por_puntaje(puntajes_por_area_1811)
#EVALUACION 20/11/2024
puntajes_por_area_2011 = leer_datos_pickle(nombre_archivo_pickle2011)
porcentajes_por_area_2011, promedios2011 = calcular_porcentajes(puntajes_por_area_2011)
puntajes_totales_2011 = generar_posiciones_por_puntaje(puntajes_por_area_2011)
#EVALUACION 22/11/2024
puntajes_por_area_2211 = leer_datos_pickle(nombre_archivo_pickle2211)
porcentajes_por_area_2211, promedios2211 = calcular_porcentajes(puntajes_por_area_2211)
puntajes_totales_2211 = generar_posiciones_por_puntaje(puntajes_por_area_2211)
#EVALUACION 25/11/2024
puntajes_por_area_2511 = leer_datos_pickle(nombre_archivo_pickle2511)
porcentajes_por_area_2511, promedios2511 = calcular_porcentajes(puntajes_por_area_2511)
puntajes_totales_2511 = generar_posiciones_por_puntaje(puntajes_por_area_2511)
#EVALUACION 27/11/2024
puntajes_por_area_2711 = leer_datos_pickle(nombre_archivo_pickle2711)
porcentajes_por_area_2711, promedios2711 = calcular_porcentajes(puntajes_por_area_2711)
puntajes_totales_2711 = generar_posiciones_por_puntaje(puntajes_por_area_2711)
#EVALUACION 29/11/2024
directorio_salida_reportes = 'reportes_29_11'
directorio_salida_graficos = 'graficos_29_11'
archivo_alumnos = 'SIMULACRO_29_11_2024.xlsx'
archivo_respuestas = 'RESPUESTAS_SIMULACRO_29_11.xlsx'
puntajes_por_area = leer_datos_pickle(nombre_archivo_pickle2911)
puntajes_totales = generar_posiciones_por_puntaje(puntajes_por_area)
porcentajes_por_area, promedios = calcular_porcentajes(puntajes_por_area)
plantilla_pdf = 'SEXTO SIMULACRO.pdf'
primeras_claves = list(porcentajes_por_area.keys())[:]
datos_envia_correo = {}

#for dni in primeras_claves:
#    # Generar el reporte
#    ruta_completa, nombre, correo = generar_reporte_pdf(directorio_salida_reportes, directorio_salida_graficos,
#                                                        dni, plantilla_pdf, dimension, espaciado_vertical, puntajes_por_area, 
#                                                        archivo_respuestas, archivo_alumnos, puntajes_totales,
#                                                        "18/11/2024", porcentajes_por_area_1811, promedios1811,
#                                                        "20/11/2024", porcentajes_por_area_2011, promedios2011,
#                                                        "22/11/2024", porcentajes_por_area_2211, promedios2211,
#                                                        "25/11/2024", porcentajes_por_area_2511, promedios2511,
#                                                        "27/11/2024", porcentajes_por_area_2711, promedios2711,
#                                                        "29/11/2024", porcentajes_por_area, promedios)
#    datos_envia_correo[dni] = [nombre, correo, ruta_completa]

#guardar_en_pickle(datos_envia_correo, "datos_encriptar_29_11.pkl")

#Guardar los puntajes y posiciones de las personas que dieron la evaluacion
# Convertir el diccionario a un DataFrame de pandas
df = pd.DataFrame.from_dict(puntajes_totales, orient='index')
# Exportar el DataFrame a un archivo Excel
df.to_excel('PUESTOS_29_11.xlsx', index=True)
print("Datos exportados a archivo_exportado.xlsx")
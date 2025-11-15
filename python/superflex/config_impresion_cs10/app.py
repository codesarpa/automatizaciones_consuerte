import config
import time
import pandas as pd
import os
import sys

# Agregar la carpeta raíz al path de búsqueda
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


from functions import (iniciar_sesion_superflex, ingresar_menu_relacion_impresora, configuracion_chance, registrar_en_excel)


iniciar_sesion_superflex()
ingresar_menu_relacion_impresora()
# crear_configuracion_chance()

df = pd.read_excel('C:/automatizaciones_consuerte/python/superflex/config_impresion_cs10/tat_cs10.xlsx')
cedulas = df['C�DULA'].tolist()

# Rutas de los archivos
ARCHIVO_PROCESADAS = "cedulas_procesadas.xlsx"
ARCHIVO_NOVEDADES = "cedulas_novedades.xlsx"

PUERTO_IMPRESION = "LPT"
TIPO_IMPRESORA_ID = "NUEVO TIPO IMPRESORA PDAS"
CEDULAS_NOVEDADES = []
CEDULAS_PROCESADAS = {}
for cedula in cedulas:
    cedula = cedula.replace("CV","")
    EQUIPO_ID = cedula
    
    for intento in range (1,3):
        if intento == 1:
            #CHANCE
            NOMBRE_INSTALACION = "PRINTER"
            MODELO_IMPRESORA_ID = "POS_CHANCE_CHANCE"
        else:
            #PAPEL BLANCO
            NOMBRE_INSTALACION = "PRINTER1"
            MODELO_IMPRESORA_ID = "IMPRESORA PARA POS PAPEL BLANCO"
        print(intento)
        print(EQUIPO_ID)
        print(PUERTO_IMPRESION)
        print(TIPO_IMPRESORA_ID)
        print(NOMBRE_INSTALACION)
        print(MODELO_IMPRESORA_ID)

        time.sleep(2)
        page.get_by_role("button", name="Crear").click()
        time.sleep(2)
        input_equipo_id = configuracion_chance()
        if not input_equipo_id:
            print(f"Error con {cedula}, pasando a la siguiente.")
            CEDULAS_NOVEDADES.append(cedula)
            ingresar_menu_relacion_impresora()
            # Registrar de inmediato en el Excel de novedades
            registrar_en_excel(
                ARCHIVO_NOVEDADES,
                [cedula, "Error al configurar"],
                ["C�DULA", "OBSERVACI�N"]
            )
            break
        else:
            CEDULAS_PROCESADAS[cedula] = input_equipo_id
            print(f"C�dula {cedula} procesada con ID {input_equipo_id}")
            # Registrar de inmediato en el Excel de procesadas
            registrar_en_excel(
                ARCHIVO_PROCESADAS,
                [cedula, input_equipo_id],
                ["C�DULA", "ID EQUIPO"]
            )

print(CEDULAS_NOVEDADES)
print(CEDULAS_PROCESADAS)
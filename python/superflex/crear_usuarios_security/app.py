from config import ENVIRONMENT,URL_SUPERFLEX_SECURITY,URL_HOME_SECURITY,USER,PASS,URL_ADMIN_USUARIOS
from playwright.sync_api import Page, expect
# from playwright import playwright 
from playwright.sync_api import sync_playwright
import re
import logging
import pandas as pd
from openpyxl import Workbook, load_workbook
import os
import time

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
page = browser.new_page()

def iniciar_sesion_superflex_security():
    logging.info("Se procede a iniciar sesion")
    try:
        #PRODUCCION
        page.goto(URL_SUPERFLEX_SECURITY)
        
        page.wait_for_timeout(5000)  # Esperar 10 segundos para que la página cargue completamente
        #USUARIO 
        page.wait_for_selector('#float-input',state='visible')
        page.fill('#float-input', USER)
        
        #CONTRASEÑA
        page.wait_for_selector('#float-input-password',state='visible')
        page.fill('#float-input-password', PASS)

        page.wait_for_timeout(5000)  # Esperar 1 segundo para que los campos se llenen
        page.get_by_text("Ingresar").click()

        page.wait_for_url(URL_HOME_SECURITY, timeout=25000)  # Ajusta 
        logging.info("Se incia sesion correctamente")
        return True
    except Exception as e:
        logging.error(f"Ocurrio un error al iniciar sesión es superflex: {e}")
        return False

def ingresar_menu_administrar_usuarios():
    try:
        page.wait_for_timeout(10000)
        # RUTA_MENU = '/sf-admin-web-comunes/admin/maestra-equipo-impresora'
        # URL_RELACION_EQUIPO_IMPRESORA = f"{URL_SUPERFLEX}{RUTA_MENU}"
        print(URL_ADMIN_USUARIOS)
        page.goto(URL_ADMIN_USUARIOS)
        # page.wait_for_timeout(10000)  # Esperar 5 segundos para que la pÃ¡gina cargue completamente
        page.wait_for_url(URL_ADMIN_USUARIOS, timeout=30000)  # Ajusta
        print("Menu Activar URL_ADMIN_USUARIOS")
        logging.info("Se ingresa al modulo de URL_ADMIN_USUARIOS")
    except Exception as e:
        print(f"â�Œ Error al ingresar URL_ADMIN_USUARIOS: {e}")
        logging.error(f"Error al ingresar URL_ADMIN_USUARIOS: {e}")

def seleccionar_empresa():
    page.wait_for_selector("p-dropdown", timeout=15000)
    page.locator("p-dropdown .p-dropdown-trigger").click()

    page.wait_for_selector(".p-dropdown-items .p-dropdown-item", timeout=10000)
    page.locator(".p-dropdown-items .p-dropdown-item").first.click()

def crear_usuarios():
    page.get_by_text("Crear").click()

    input_identificacion = page.get_by_placeholder("Escribir Identificación (*)")
    input_identificacion.wait_for(state='visible')
    input_identificacion.fill(f"{vincedula}")

    input_primer_nombre = page.get_by_placeholder("Escribir Primer nombre (*)")
    input_primer_nombre.wait_for(state='visible')
    input_primer_nombre.fill(f"{primer_nombre}")

    input_segundo_nombre = page.get_by_placeholder("Escribir Segundo nombre")
    input_segundo_nombre.wait_for(state='visible')
    input_segundo_nombre.fill(f"{segundo_nombre}")
    
    input_primer_apellido = page.get_by_placeholder("Escribir Primer apellido (*)")
    input_primer_apellido.wait_for(state='visible')
    input_primer_apellido.fill(f"{primer_apellido}")
    
    input_segundo_apellido = page.get_by_placeholder("Escribir Segundo apellido")
    input_segundo_apellido.wait_for(state='visible')
    input_segundo_apellido.fill(f"{segundo_apellido}")

    input_correo = page.get_by_placeholder("Escribir Correo electrónico")
    input_correo.wait_for(state='visible')
    input_correo.fill(f"{vinemail}")
    
    input_correo_confirmar = page.get_by_placeholder("Escribir Confirmar Correo electrónico")
    input_correo_confirmar.wait_for(state='visible')
    input_correo_confirmar.fill(f"{vinemail}")

    #CONFIGURACION
    page.locator("label:has-text('Activo')").locator("..").locator("p-checkbox .p-checkbox-box").click()

    input('ENTER PARA GUARDAR')
    page.get_by_text("Guardar").click()
    input('ENTER PARA LIMPIAR')
    # page.get_by_text("Limpiar").click()

if iniciar_sesion_superflex_security():
    ingresar_menu_administrar_usuarios()
    seleccionar_empresa()

    #LEER ARCHIVO CSV 
    ARCHIVO = 'C:/automatizaciones_consuerte/python/superflex/crear_usuarios_security/robots_maicol.csv'
    df = pd.read_csv(ARCHIVO, sep=";", encoding="utf-8")
    print(df.columns)

    for index, fila in df.iterrows():
        vincedula = str(fila['vincedula'] or "")
        primer_nombre = str(fila['primer_nombre'] or "")
        segundo_nombre = str(fila['segundo_nombre'] or "")
        primer_apellido = str(fila['primer_apellido'] or "")
        segundo_apellido = str(fila['segundo_apellido'] or "")
        vinemail = str(fila['vinemail'] or "")
        vinnombre = str(fila['vinnombre'] or "")
        print(f"{vincedula} - {primer_nombre} {segundo_nombre} - {primer_apellido} - {segundo_apellido} - {vinemail} - {vinnombre}")
        crear_usuarios()
    input("ENTER PARA TERMINAR")
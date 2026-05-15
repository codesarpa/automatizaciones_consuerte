from config import ENVIRONMENT,URL_USUARIOS_BODEGAS,URL_SUPERFLEX,URL_HOME,USER,PASS, URL_ADMIN_USUARIOS, logs_diarios
from playwright.sync_api import Page, expect
# from playwright import playwright 
from playwright.sync_api import sync_playwright
import re
# import logging
import pandas as pd
from openpyxl import Workbook, load_workbook
import os
import time

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
page = browser.new_page()

logs = logs_diarios()
log = logs[0]


def iniciar_sesion_superflex():
    log.info("Se procede a iniciar sesion")
    try:
        #PRODUCCION
        print(URL_SUPERFLEX)
        page.goto(URL_SUPERFLEX)
        
        page.wait_for_timeout(10000)  # Esperar 10 segundos para que la p�gina cargue completamente
        #USUARIO 
        page.wait_for_selector('#float-input',state='visible')
        page.fill('#float-input', USER)
        
        #CONTRASEnA
        page.wait_for_selector('#float-input-password',state='visible')
        page.fill('#float-input-password', PASS)

        page.wait_for_timeout(10000)  # Esperar 1 segundo para que los campos se llenen
        page.get_by_text("Ingresar").click()

        page.wait_for_url(URL_HOME, timeout=25000)  # Ajusta 
        log.info("Se incia sesion correctamente")
        print("Login exitoso")
        return True
    except Exception as e:
        log.error(f"Ocurrio un error al iniciar sesi�n es superflex: {e}")

def ingresar_menu_usuarios_bodegas():
    try:
        page.goto(URL_USUARIOS_BODEGAS)

        # page.wait_for_timeout(10000)
        # page.locator("span.layout-menuitem-text", has_text="ADMINISTRACI�N").click()
        # page.wait_for_timeout(1000)  # Esperar un poco
        # page.locator("span.layout-menuitem-text", has_text="USUARIOS").click()
        # page.wait_for_timeout(1000)  # Esperar un poco
        # page.locator("span.layout-menuitem-text", has_text="Administraci�n de usuarios").click()

        page.wait_for_url(URL_ADMIN_USUARIOS, timeout=30000)  # Ajusta
        print("se ingresa al URL_USUARIOS_BODEGAS")
        # log.info("Se ingresa al modulo de URL_ADMIN_USUARIOS")
    except Exception as e:
        print(f"Error al ingresar URL_ADMIN_USUARIOS: {e}")
        log.error(f"Error al ingresar URL_ADMIN_USUARIOS: {e}")

if iniciar_sesion_superflex():
    # ingresar_menu_administrar_usuarios()
    ingresar_menu_usuarios_bodegas()
    # recorrer_usuarios()
    input("ENTER PARA FINALIZAR")
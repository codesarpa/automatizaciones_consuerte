from config import ENVIRONMENT,URL_SUPERFLEX_SECURITY,URL_HOME_SECURITY,USER,PASS,URL_ADMIN_USUARIOS, logs_diarios
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

logs = logs_diarios()
log = logs[0]

# vinemail = "primitivoave@gmail.com"
# vincedula = ''

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
    log.info("Se selecciona la empresa")

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

def consultar_usuarios():
    #INPUT PARA CONSULTAR CEDULA DE USUARIO
    log.info("Se prepara para consultar el siguiente usuario:")
    log.info(f"{vincedula} - {vinnombre} - {vinemail}")
    inputs = page.locator("input.p-inputtext")
    time.sleep(2)
    input_identificacion = inputs.nth(1)
    input_identificacion.click()
    input_identificacion.fill(f'{vincedula}')
    input_identificacion.press("Enter")
    log.info(f"Se consultó el usuario: {vincedula}")

    time.sleep(2)
    checkbox = page.locator("div[role='checkbox'].p-checkbox-box.p-component").first
    checkbox.click()

    page.get_by_role("button", name="Editar").click()
    log.info("Se ingresa a editar usuario")
    # page.locator(".p-inputtext").first.click()

def actualizar_correo_usuario():
    diligenciar_formulario()
    validar_formulario()
    

def diligenciar_formulario():
    log.info(f"Se prepara para escribir el correo: {vinemail}")
    time.sleep(3)
    input_correo = page.get_by_placeholder("Escribir Correo electrónico")
    input_correo.wait_for(state='visible')
    input_correo.fill(f"{vinemail}")
    log.info(f"Se escribió el correo: {vinemail}")


    log.info(f"Se prepara para confirmar el correo: {vinemail}")
    time.sleep(3)
    input_correo_confirmar = page.get_by_placeholder("Escribir Confirmar Correo electrónico")
    input_correo_confirmar.wait_for(state='visible')
    input_correo_confirmar.fill(f"{vinemail}")
    log.info(f"Se confirma el correo: {vinemail}")
    time.sleep(3)

    #
    # input("Hola")
    # page.get_by_role("option", name="Activo").click()
    # page.get_by_placeholder("Escribir Primer nombre (*)")
    page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-usuario-ms/sf-card/div/form/app-form-usuario/form/div[9]/sf-dropdown/p-dropdown").click()
    time.sleep(2)

    page.locator("li[role='option'][aria-label='Activo']").click()
    time.sleep(2)

    input_usu_externo = page.get_by_placeholder("Escribir Usuario Externo")
    input_usu_externo.wait_for(state='visible')
    input_usu_externo.fill(f"{vincedula}")

    #ZONA HORARIA
    page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-usuario-ms/sf-card/div/form/app-form-usuario/form/div[11]/sf-dropdown/p-dropdown").click()
    time.sleep(2)

    page.locator("li.p-dropdown-item:has-text('(UTC-05:00) América/Bogota - Colombia')").click()

def validar_formulario():
    #validar si se escribieron correctamente los valores:
    max_intentos=3
    for intento in range(max_intentos):
        input_correo = page.get_by_placeholder("Escribir Correo electrónico")
        texto_correo = input_correo.input_value()

        if texto_correo == vinemail:
            log.info(f"Correo actualizado correctamente: {texto_correo}")
            page.get_by_text("Actualizar").click()
            time.sleep(5)

            #validar si se carga el campo identificacion:
            try:
                # inputs = page.locator("input.p-inputtext")
                xpath_input_ident = '/html/body/app-root/app-main/div/div[1]/div/app-usuario-ms/sf-card/div/form/section[2]/sf-table-filtro-cabecera/p-table/div/div/table/thead/tr/th[2]/input'
                page.wait_for_selector(f"xpath={xpath_input_ident}", timeout=7000)
                log.info("Campo de identificación encontrado. Actualización exitosa.")
                time.sleep(2)
                return True
                # input_identificacion = inputs.nth(1)
            except Exception as e:
                log.error("No se encontró el campo de identificación tras actualizar.")
                return False
            
        else:
            log.info(f"Intento {intento+1}: no coincidió ({texto_correo}) → reintentando...")
            diligenciar_formulario()
            time.sleep(2)

    log.error("No se pudo actualizar el correo después de varios intentos.")
    return False


if iniciar_sesion_superflex_security():
    # input("PERE")
    ingresar_menu_administrar_usuarios()
    seleccionar_empresa()

    #LEER ARCHIVO CSV 
    ARCHIVO = 'C:/automatizaciones_consuerte/python/superflex/actualizar_correo_usuarios/cedulas_correos.xlsx'
    df = pd.read_excel(ARCHIVO)
    print(df.columns)

    for index, fila in df.iterrows():
        vincedula = str(fila['VINCEDULA'] or "")
        vinnombre = str(fila['VINNOMBRE'] or "")
        vinemail = str(fila['VINEMAIL'] or "")
        estado = str(fila['ESTADO'] or "")
        print(f"{vincedula} - {vinnombre} - {vinemail}")
        print(repr(fila['ESTADO']))
        if estado == "1.0":
            log.info(f"usuario en estado 1, se continua con el siguiente registro")
            print(f"usuario en estado 1, se continua con el siguiente registro")
            continue
    
        consultar_usuarios()
        # actualizar_correo_usuario()
        diligenciar_formulario()
        if validar_formulario():
            print("Se actualiza correctamente")
        else:
            print("Error al actualizar el usuario")
            log.info(f"Error al actualizar el usuario")
            df.loc[index, 'RESULTADO'] = 0
            page.screenshot(path=f"{vincedula}.png")
            page.get_by_role("button", name="Cancelar").click()

        # input("CANCELAR PARA CONSULTAR EL SIGUIENTE USUARIO")
        time.sleep(2)
        # page.get_by_role("button", name="Cancelar").click()
        df.to_excel(ARCHIVO, index=False)

    #     crear_usuarios()
    input("ENTER PARA TERMINAR")
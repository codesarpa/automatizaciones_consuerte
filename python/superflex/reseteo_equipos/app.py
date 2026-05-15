from config import ENVIRONMENT,URL_SUPERFLEX,URL_HOME,USER,PASS, URL_ADMIN_USUARIOS, logs_diarios
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

def ingresar_menu_administrar_usuarios():
    try:
        page.wait_for_timeout(10000)
        page.locator("span.layout-menuitem-text", has_text="ADMINISTRACI�N").click()
        page.wait_for_timeout(1000)  # Esperar un poco
        page.locator("span.layout-menuitem-text", has_text="USUARIOS").click()
        page.wait_for_timeout(1000)  # Esperar un poco
        page.locator("span.layout-menuitem-text", has_text="Administraci�n de usuarios").click()

        page.wait_for_url(URL_ADMIN_USUARIOS, timeout=30000)  # Ajusta
        print("se ingresa al URL_ADMIN_USUARIOS")
        log.info("Se ingresa al modulo de URL_ADMIN_USUARIOS")
    except Exception as e:
        print(f"Error al ingresar URL_ADMIN_USUARIOS: {e}")
        log.error(f"Error al ingresar URL_ADMIN_USUARIOS: {e}")

def ir_a_pagina(page, num_pagina):
    try:
        print(f"Intentando ir a la p�gina {num_pagina}...")
        log.info(f"Intentando ir a la p�gina {num_pagina}...")

        # Intenta hasta 200 veces avanzar si la p�gina no est� visible
        for _ in range(200):
            botones = page.locator("button.p-paginator-page")
            total_botones = botones.count()

            # Buscar si la p�gina deseada est� visible
            for i in range(total_botones):
                texto = botones.nth(i).inner_text().strip()
                if texto == str(num_pagina):
                    botones.nth(i).click()
                    page.wait_for_function(
                        """() => document.querySelectorAll('tbody tr').length > 0""",
                        timeout=20000
                    )
                    print(f"P�gina {num_pagina} abierta correctamente.")
                    log.info(f"P�gina {num_pagina} abierta correctamente.")
                    return True

            # Si no aparece, presionar el bot�n "siguiente"
            siguiente = page.locator("button.p-paginator-next")
            if siguiente.is_enabled():
                siguiente.click()
                page.wait_for_timeout(1000)
            else:
                print(f"Fin de paginaci�n alcanzado antes de llegar a {num_pagina}.")
                log.info(f"Fin de paginaci�n alcanzado antes de llegar a {num_pagina}.")
                return False

        print(f"No se encontr� la p�gina {num_pagina} despu�s de varios intentos.")
        log.info(f"No se encontr� la p�gina {num_pagina} despu�s de varios intentos.")
        return False

    except Exception as e:
        print(f"Error al intentar ir a la p�gina {num_pagina}: {e}")
        log.info(f"Error al intentar ir a la p�gina {num_pagina}: {e}")
        return False


def recorrer_usuarios():
    # Esperar que la tabla est� visible
    page.wait_for_selector("table")
    time.sleep(5)
    print("esperando")
    log.info("esperando")

    pagina_actual = 129  # contador manual de p�ginas
    ir_a_pagina(page, pagina_actual)
    while True:
        print(f"Procesando p�gina {pagina_actual}...")
        filas = page.locator("tbody tr")
        total = filas.count()
        print(f"Total de filas encontradas: {total}")
        log.info(f"Total de filas encontradas: {total}")

        for i in range(total):
            time.sleep(2)
            fila = filas.nth(i)

            # Buscar el �cono de estado
            estado_label = fila.locator("label.p-d-flex")
            color = estado_label.evaluate("el => getComputedStyle(el).color")

            print(f"Fila {i+1} - color: {color}")
            log.info(f"Fila {i+1} - color: {color}")

            if "45, 172, 49" in color:
                # Click en el radio visible
                radio_button = fila.locator(".p-radiobutton-box")
                radio_button.wait_for(state="visible")
                radio_button.click()
                print(f"Clic en radio de fila {i + 1}")
                log.info(f"Clic en radio de fila {i + 1}")

                # Editar y actualizar
                time.sleep(2)
                page.get_by_text("Editar").click()
                time.sleep(2)

                # page.get_by_text("Actualizar").click()
                
                actualizar_btn = page.get_by_role("button", name="Actualizar")
                page.wait_for_selector("button:has-text('Actualizar')", state="visible", timeout=10000)

                # Esperar hasta 10 segundos que se habilite el bot�n
                for _ in range(20):  # 20 x 0.5 = 10 segundos
                    if actualizar_btn.is_enabled():
                        actualizar_btn.click()
                        print("Registro actualizado correctamente")
                        log.info("Registro actualizado correctamente")
                        break
                    time.sleep(0.5)
                else:
                    # Si despu�s de 10 segundos sigue deshabilitado:
                    # Esperar a que desaparezca el loader (si existe)
                    try:
                        page.wait_for_selector("app-loader", state="detached", timeout=15000)
                    except:
                        print("El loader no desapareci� a tiempo, intentando continuar de todas formas...")
                        log.info("El loader no desapareci� a tiempo, intentando continuar de todas formas...")

                    # Ahora s� intentar hacer clic en 'Cancelar'
                    page.get_by_text("Cancelar").click()
                    time.sleep(2)
                    print("No se encuentra habilitado el bot�n actualizar.")
                    log.info("No se encuentra habilitado el bot�n actualizar.")
                    radio_button.click()
                    print(f"Dando click nuevamente en radio de la fila {i + 1}.")
                    log.info(f"Dando click nuevamente en radio de la fila {i + 1}.")

                print("Registro actualizado.")
                log.info("Registro actualizado.")

                # Esperar que recargue la tabla
                page.wait_for_function(
                    """() => document.querySelectorAll('tbody tr').length > 0""",
                    timeout=20000
                )


                # Validar si la actualizaci�n devolvi� a la primera p�gina
                try:
                    activo = page.locator("button.p-paginator-page.p-highlight").inner_text().strip()
                    pagina_visible = int(activo)

                    if pagina_visible != pagina_actual:
                        print(f"Regres� a la p�gina {pagina_visible}, volviendo a {pagina_actual}...")
                        ir_a_pagina(page, pagina_actual)
                        time.sleep(2)
                except Exception as e:
                    print(f"Error al validar la p�gina activa: {e}")
            else:
                print(f"Fila {i + 1}: inactiva, se omite")
                log.error(f"Fila {i + 1}: inactiva, se omite")

        # Avanzar a la siguiente p�gina
        try:
            next_button = page.locator("button.p-paginator-next")
            time.sleep(2)
            next_button.wait_for(state="visible", timeout=10000)
            time.sleep(1)

            if next_button.is_enabled():
                next_button.click()
                pagina_actual += 1
                print(f"Avanzando a la p�gina {pagina_actual}...")
                page.wait_for_selector("tbody tr", state="visible", timeout=10000)
                time.sleep(2)
            else:
                print("No hay m�s p�ginas disponibles.")
                break
        except Exception as e:
            print(f"Error al hacer clic en 'Siguiente': {e}")
            break


    # page.get_by_text("Editar").click()


if iniciar_sesion_superflex():
    # ingresar_menu_administrar_usuarios()
    # recorrer_usuarios()
    input("ENTER PARA FINALIZAR")
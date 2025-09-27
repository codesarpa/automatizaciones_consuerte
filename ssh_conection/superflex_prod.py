from playwright.sync_api import Page, expect
# from playwright import playwright 
from playwright.sync_api import sync_playwright
import re
import logging
import pandas as pd

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
page = browser.new_page()
    
logging.basicConfig(
    filename='Logs_ejecucion.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


URL_PROD='https://prod-superflex-admin.codesa.com.co'

def iniciar_sesion():
    logging.info("Se procede a iniciar sesión")
    try:
        #PRODUCCION
        page.goto(URL_PROD)
        
        page.wait_for_timeout(20000)  # Esperar 10 segundos para que la página cargue completamente
        # Ingresar las credenciales
        page.wait_for_selector('#float-input')
        page.fill('#float-input', '1007420377')
        # PRODUCCION
        page.fill('#float-input-password', 'SW123')
        # PRUEBAS
        # page.fill('#float-input-password', 'cp789')
        
        page.wait_for_timeout(10000)  # Esperar 1 segundo para que los campos se llenen
        page.get_by_text("Ingresar").click()
        # PRODUCCION
        page.wait_for_url("https://prod-superflex-admin.codesa.com.co/app/admin/home", timeout=25000)  # Ajusta 
        logging.info("Se incia sesión correctamente")
        print("✅ Login exitoso")
    except Exception as e:
        logging.error(f"Ocurrio un error al iniciar sesión es superflex: {e}")

def ingresar_menu_activar_servicios():
    try:
        page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
        URL_SERV = '/sf-admin-web-comunes/admin/servicios'
        page.goto(URL_PROD+URL_SERV)
        page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
        page.wait_for_url(URL_PROD+URL_SERV, timeout=30000)  # Ajusta
        print("✅ Menu Activar Servicios")
        logging.info("Se ingresa al modulo de Activar Servicios")
    except Exception as e:
        print(f"❌ Error al ingresar al menu de activar servicios: {e}")
        logging.error(f"Error al ingresar al menu de activar servicios: {e}")

def ingresar_menu_relacion_impresora():
    try:
        page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
        URL_IMP = '/sf-admin-web-comunes/admin/maestra-equipo-impresora'
        page.goto(URL_PROD+URL_IMP)
        page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
        page.wait_for_url(URL_PROD+URL_IMP, timeout=30000)  # Ajusta
        print("✅ Menu Activar Servicios")
        logging.info("Se ingresa al modulo de Relacion equipo Impresora")
    except Exception as e:
        print(f"❌ Error al ingresar al menu de relacion equipo impresora: {e}")
        logging.error(f"Error al ingresar al menu de relacion equipo impresora : {e}")

def activar_servicios(pdv):
    try:
        # Servicio - VALIDAR ESTADO IMPRESORA EN EL POS
        #PRODUCCION
        page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[1]/p-dropdown/div').click()
        # PRUEBAS
        # page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[1]/p-dropdown/div').click()
        page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
        page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[1]/p-dropdown/div/div[3]/div[2]/ul/p-dropdownitem[99]/li').click()

        # Tecnología - SUPERFLEX
        page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[2]/sf-dropdown/p-dropdown/div').click()
        page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
        page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[2]/sf-dropdown/p-dropdown/div/div[3]/div/ul/p-dropdownitem[1]/li').click()

        # Jerarquía - Punto de Venta
        page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[3]/sf-rango-jerarquia-maestra/div/div[1]/p-dropdown/div').click()
        page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
        page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[3]/sf-rango-jerarquia-maestra/div/div[1]/p-dropdown/div/div[3]/div/ul/cdk-virtual-scroll-viewport/div[1]/p-dropdownitem[9]/li').click()

        # BUSCADOR PUNTO DE VENTA 
        page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[3]/sf-rango-jerarquia-maestra/div/div[2]/sf-input-buscador-maestra-jerarquia/div/button').click()
        
        # INPUT BUSCADOS PUNTO DE VENTA
        # page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[3]/sf-rango-jerarquia-maestra/div/div[1]/p-dropdown/div').click()
        page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
        page.fill('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[3]/sf-rango-jerarquia-maestra/div/div[2]/sf-input-buscador-maestra-jerarquia/sf-modal-buscador-maestra/p-dialog/div/div/div[2]/form/div/div[1]/div/sf-table-filtro-cabecera/p-table/div/div/table/thead/tr/th[2]/input', pdv)
        page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[3]/sf-rango-jerarquia-maestra/div/div[2]/sf-input-buscador-maestra-jerarquia/sf-modal-buscador-maestra/p-dialog/div/div/div[2]/form/div/div[1]/div/sf-table-filtro-cabecera/p-table/div/div/table/thead/tr/th[2]/input').press('Enter')
        # page.press('Enter')
        
        # BUSCADOR PUNTO DE VENTA
        page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/form/div/div[3]/sf-rango-jerarquia-maestra/div/div[2]/sf-input-buscador-maestra-jerarquia/sf-modal-buscador-maestra/p-dialog/div/div/div[2]/form/div/div[1]/div/sf-table-filtro-cabecera/p-table/div/div/table/tbody/tr/td[1]/p-tableradiobutton/div/div[2]').click()
        page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
        
        # BOTON BUSCAR
        page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/sf-card/div/div[1]/div/div/sf-buscar-btn/p-button/button').click()
        print("Boton Buscar")
        # VERIFICAR VENTANA EMERGENTE
        try:
            page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
            aceptar_btn = page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/p-confirmdialog[2]/div/div/div[3]/button[2]')
            aceptar_btn.wait_for(timeout=10000)
            logging.info("Ventada emergente detectada")
            aceptar_btn.click()
            logging.info("Se da click al botón")
        except:
            logging.info("No se encuentra ventana emergente")
            
        # VERIFICAR CHECKBOX
        try:
            page.wait_for_timeout(timeout=10000)
            checkbox = page.locator("p-checkbox >> div.p-checkbox")
            checkbox.wait_for(timeout=10000)
            is_checked = "p-checkbox-checked" in checkbox.get_attribute("class")
            
            if is_checked:
                logging.info("El checkbox esta marcado.")
                return "El checkbox esta marcado."
            else:
                logging.error("El checkbox NO esta marcado, se procede a dar click..")
                page.locator("p-checkbox >> div.p-checkbox-box").click()
                try:
                    page.wait_for_timeout(9000)    
                    # btn_config = page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-activar-servicio/p-confirmdialog[1]/div/div/div[3]/button[2]")
                    page.get_by_role("button", name="Sobrescribir").click()
                    # btn_config.wait_for(timeout=5000)
                    # btn_config.click()
                    logging.info("Se da click en el boton de confirmacion de activacion")
                    
                except:
                    logging.info("Fallo al dar click en el boton de confirmacion de activacion")
                
                # Esperamos un pequeño tiempo para asegurar que el cambio se aplique
                page.wait_for_timeout(10000)    
                # Verificamos nuevamente
                is_now_checked = "p-checkbox-checked" in checkbox.get_attribute("class")

                if is_now_checked:
                    logging.info("Checkbox marcado exitosamente.")
                    return "Checkbox marcado exitosamente."
                else:
                    logging.info("Intento fallido: El checkbox sigue sin marcar.")
                    return "Intento fallido: El checkbox sigue sin marcar."
        except:
            logging.critical("No se encontró el checkbox.")
            return "No se encontró el checkbox."
        # page.wait_for_url("https://prod-superflex-admin.codesa.com.co/sf-admin-web-comunes/admin/servicios/activar-servicios", timeout=10000)  # Ajusta según tu app
    except Exception as e:
        print(f"❌ Error en el modulo de activar servicios: {e}")

def config_impresoras(cod):
    try:
        logging.info("Se ingresa a la configuracion de impresora")
        # INPUT EQUIPO ID
        page.fill('xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/div[2]/div/div/sf-table-filtro-cabecera-maestra/form/p-table/div/div/table/thead/tr/th[6]/div[2]/sf-input-buscador-maestra/div/input', cod)
        page.wait_for_timeout(9000)  # Esperar 5 segundos para que la página cargue completamente
        
        page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/div[2]/div/div/sf-table-filtro-cabecera-maestra/form/p-table/div/div/table/thead/tr/th[6]/div[2]/sf-input-buscador-maestra/div/input').press('Enter')
        
        page.wait_for_timeout(8000)  # Esperar 5 segundos para que la página cargue completamente

        puerto_impresion_gamble = page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/div[2]/div/div/sf-table-filtro-cabecera-maestra/form/p-table/div/div/table/tbody/tr[1]/td[2]").inner_text().strip()
        puerto_impresion_giros = page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/div[2]/div/div/sf-table-filtro-cabecera-maestra/form/p-table/div/div/table/tbody/tr[2]/td[2]").inner_text().strip()
        
        print(puerto_impresion_gamble)
        print(puerto_impresion_giros)
        
        print(f"✅ Puerto impresión de gamble: '{puerto_impresion_gamble}'")
        logging.info(f"Puerto impresión de gamble: '{puerto_impresion_gamble}'")
        if puerto_impresion_gamble != "/dev/usb/lp0":
            puerto_gamble = "/dev/usb/lp0"
            logging.info(f"Se procede a cambiar el puerto impresion por: {puerto_gamble}")
            page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
            # RADIO BUTTON
            page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/div[2]/div/div/sf-table-filtro-cabecera-maestra/form/p-table/div/div/table/tbody/tr[1]/td[1]/p-radiobutton/div/div[2]").click()
            page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
            #EDITAR
            page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/div[2]/div/div/sf-table-filtro-cabecera-maestra/div/div/div[2]/button").click()
            # CAMPO PUUUERTO IMPRESION
            page.wait_for_timeout(9000)  # Esperar 5 segundos para que la página cargue completamente
            page.fill("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/form/div/div[1]/div[1]/sf-input-text/input", puerto_gamble)
            page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/form/div/div[1]/div[1]/sf-input-text/input").press('Enter')
            page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
            page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/form/div/div[2]/div/sf-confirmar-general-btn/p-button/button").click()
            page.wait_for_timeout(8000)  # Esperar 5 segundos para que la página cargue completamente
            #BOTON MODAL CONFIRMACION
            page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/p-confirmdialog/div/div/div[3]/button[2]').click()
            page.wait_for_timeout(8000)  # Esperar 5 segundos para que la página cargue completamente
            
            logging.info("Se cambia el valor de puerto de impresion de gamble correctamente")
            #     input("Hola, presiona Enter para continuar...")
        logging.info(f"Puerto impresión de giros: '{puerto_impresion_giros}'")
        
        if puerto_impresion_giros != "/dev/usb/lp1":
            puerto_giros = "/dev/usb/lp1"
            logging.info(f"Se procede a cambiar el puerto impresion por: {puerto_giros}")
            page.wait_for_timeout(8000)  # Esperar 5 segundos para que la página cargue completamente
            page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/div[2]/div/div/sf-table-filtro-cabecera-maestra/form/p-table/div/div/table/tbody/tr[2]/td[1]/p-radiobutton/div/div[2]").click()
            page.wait_for_timeout(10000)  # Esperar 5 segundos para que la página cargue completamente
            page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/div[2]/div/div/sf-table-filtro-cabecera-maestra/div/div/div[2]/button").click()
            page.wait_for_timeout(8000)  # Esperar 5 segundos para que la página cargue completamente
            page.fill("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/form/div/div[1]/div[1]/sf-input-text/input", puerto_giros)
            page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/form/div/div[1]/div[1]/sf-input-text/input").press('Enter')
            page.wait_for_timeout(8000)  # Esperar 5 segundos para que la página cargue completamente
            page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/form/div/div[2]/div/sf-confirmar-general-btn/p-button/button").click()
            page.wait_for_timeout(8000)  # Esperar 5 segundos para que la página cargue completamente
            #BOTON MODAL CONFIRMACION
            page.locator('xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/p-confirmdialog/div/div/div[3]/button[2]').click()
            page.wait_for_timeout(8000)  # Esperar 5 segundos para que la página cargue completamente
            logging.info("Se cambia el valor de puerto de impresion de giros correctamente")
            
            logging.info("Se validan nuevamente los valores de puerto de impresion:")
            puerto_impresion_gamble = page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/div[2]/div/div/sf-table-filtro-cabecera-maestra/form/p-table/div/div/table/tbody/tr[1]/td[2]").inner_text().strip()
            puerto_impresion_giros = page.locator("xpath=/html/body/app-root/app-main/div/div[1]/div/app-equipo-impresora/sf-formulario-maestra/div[2]/div/div/sf-table-filtro-cabecera-maestra/form/p-table/div/div/table/tbody/tr[2]/td[2]").inner_text().strip()
            logging.info(f"puerto impresion gamble: {puerto_impresion_gamble}")
            logging.info(f"puerto impresion giros: {puerto_impresion_giros}")


        return puerto_impresion_gamble, puerto_impresion_giros
    except Exception as e:
        print(f"❌ Error en el modulo de configurar impresoras: {e}")
        return "Error"

logging.info("------------------------------------")
logging.info("SE INICIA EL PROCESO")
logging.info("------------------------------------")
iniciar_sesion()
# ingresar_menu_activar_servicios()
# ingresar_menu_relacion_impresora()
df = pd.read_excel("codigos_superflex.xlsx")
# Iterar registros
for idx, row in df.iterrows():
    nombre_pdv = str(row["NOMBRE PDV"]).strip()
    cod_superflex = str(row["COD SUPERFLEX"]).strip()
    cod_impresora = str(row["COD IMPRESORA"]).strip()

    logging.info(f"Se inicia el proceso con el pdv: {nombre_pdv}")
    ingresar_menu_activar_servicios()
    estado_activacion = activar_servicios(cod_superflex)
    ingresar_menu_relacion_impresora()
    puerto_gamble, puerto_giros = config_impresoras(cod_impresora)
    
    # Escribir resultados en las columnas correspondientes
    df.at[idx, "PUERTO GAMBLE"] = puerto_gamble
    df.at[idx, "PUERTO GIROS"] = puerto_giros
    df.at[idx, "ESTADO ACTIVACION"] = estado_activacion
    
    logging.info(f"Se finaliza el proceso con el pdv: {nombre_pdv}")
# Guardar el Excel actualizado (puedes sobrescribir o crear nuevo)
df.to_excel("codigos_superflex.xlsx", index=False)
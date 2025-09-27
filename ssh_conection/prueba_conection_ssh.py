import logging
import paramiko
import re
import pandas as pd
from playwright.sync_api import Page, expect
# from playwright import playwright 
from playwright.sync_api import sync_playwright


logging.basicConfig(
    filename='Logs.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


def iniciar_sesion():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://prod-superflex-admin.codesa.com.co/login")

    page.wait_for_timeout(10000)  # Esperar 10 segundos para que la página cargue completamente

    # Ingresar las credenciales
    page.wait_for_selector('#float-input')
    page.fill('#float-input', '1007420377')
    page.fill('#float-input-password', 'SW123')
    # page.fill('input[name="password"]', 'consuerte')
    # page.get_by_test_id("float-input").fill("1007420377")
    # page.get_by_test_id("float-input-password").fill("SW123")
    page.wait_for_timeout(1000)  # Esperar 1 segundo para que los campos se llenen
    page.get_by_text("Ingresar").click()
    # page.locator("/html/body/app-root/app-login/div/div/div[2]/div/form/div/div[3]/button").click()
    # Esperar redirección a otra página
    page.wait_for_url("https://prod-superflex-admin.codesa.com.co/app/admin/home", timeout=10000)  # Ajusta según tu app

    print("✅ Login exitoso")

    input("Hola, presiona Enter para continuar...")
    # Navegar a la URL deseada
    # page.screenshot(path="hol.png")

comandos = [
    'ip link show enp1s0 | grep ether', #obtener mac
]

# host = '10.8.0.231'
# host = '10.8.0.157'
# host = '10.8.0.156'
# host = '10.8.0.159'

# host = '10.2.13.244' # NO CONECTA
# host = '10.2.13.170'
# host = '10.2.13.202'
# host = '10.2.13.212'
# host = '10.2.13.40'
host = '10.2.13.200' #HOLA COMO ESTAS

username = 'gamble'
password = 'consuerte'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"🔌 Conectando a {host}")
    ssh.connect(host, port=22, username=username, password=password)

    comando = 'ip a'
    stdin, stdout, stderr = ssh.exec_command(comando)
    salida = stdout.read().decode()
    error = stderr.read().decode()
    print(salida)

    if error:
        print(f"❌ Error al ejecutar el comando: {error}")
    elif salida.strip() == "":
        print("⚠️ No se obtuvo salida. Puede que la interfaz no exista.")
    else:
        mac = None
        interfaz_actual = None

        bloques = salida.split("\n")
        for i in range(len(bloques)):
            linea = bloques[i].strip()

            # Detecta el nombre de la interfaz Ethernet, activa o no
            match_interfaz = re.match(r'^\d+:\s+(\w+):', linea)
            if match_interfaz:
                interfaz_actual = match_interfaz.group(1)

                # Buscar la línea con la MAC justo debajo de la interfaz
                for j in range(i+1, i+5):  # Revisa algunas líneas siguientes
                    if j < len(bloques):
                        match_mac = re.search(r'link/ether\s+([0-9a-fA-F:]{17})', bloques[j])
                        if match_mac:
                            mac = match_mac.group(1)
                            break

                if mac:
                    break

        if mac and interfaz_actual:
            print(f"✅ MAC de interfaz Ethernet ({interfaz_actual}): {mac}")
            # iniciar_sesion()
        else:
            print("⚠️ No se encontró ninguna interfaz Ethernet con MAC.")
except Exception as e:
    print(f"❌ Error general: {e}")

finally:
    ssh.close()
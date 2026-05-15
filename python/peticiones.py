import requests
import cgi
import base64
def iniciar_sesion():
    session = requests.Session()
        
    url = "http://186.117.156.122:8082/Bonos/IniciarSesion"

    payload = {
        'id_usuario': '800159687',
        'pwd_usuario': 'C0ns43rt3'
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
    # Realizamos la petición POST
        response = session.post(url, data=payload, headers=headers, timeout=10)
        
        # Verificamos si la petición fue exitosa (Status Code 200)
        if response.status_code == 200:
            print("Petición enviada exitosamente.")
            # print("Respuesta del servidor:", response.text)
            print("Respuesta del servidor:", response)
            return session
        else:
            print(f"Error en la petición. Código de estado: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error de conexión: {e}")

def descargar_reporte(session):

    nombre_archivo="reporte_pagos.xlsx"
    url = "http://186.117.156.122:8082/Bonos/GenerarArchivoPagosC"

    payload = {
        'fecini': '2026/03/02',
        'fecfin': '2026/03/02'
    }


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Usamos stream=True para descargas de archivos
    try:
        # Usamos la sesión para pedir el archivo
        response = session.post(url, data=payload, stream=True, timeout=30)
            # r.raise_for_status() # Lanza error si el status no es 200
        
        content_disposition = response.headers.get('Content-Disposition')

        if content_disposition:
            value, params = cgi.parse_header(content_disposition)
            nombre_archivo = params.get('filename', 'nombre_por_defecto.xlsx')
            # Limpiar posibles comillas del nombre
            nombre_archivo = nombre_archivo.replace('"', '')
        else:
            print("El servidor no envió un nombre específico. Usando genérico.")
            nombre_archivo = "reporte_generico.xlsx"

        with open(nombre_archivo, "wb") as f:
           for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Archivo descargado con su nombre original: {nombre_archivo}")
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error de conexión: {e}")


def iniciar_sesion_brinks():
    session = requests.Session()
        
    url = "https://www.24sevenbrinks.com/api/v1/account/login"
# rdiaz@consuerte.com.co
# C0nsu2025#
    payload = {
        'password': 'C0nsu2025#',
        'username': 'rdiaz@consuerte.com.co'
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json"
    }

    try:
    # Realizamos la petición POST
        response = session.post(url, json=payload, headers=headers, timeout=10)
        
        # Verificamos si la petición fue exitosa (Status Code 200)
        if response.status_code == 200:
            print("Petición enviada exitosamente.")
            # print("Respuesta del servidor:", response.text)
            print("Respuesta del servidor:", response.json())
            return session
        else:
            print(f"Error en la petición. Código de estado: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error de conexión: {e}")


def descargar_reporte_brinks(session):
    print("asdf")

    nombre_archivo="reporte_depositos_brinks.xlsx"
    url = "https://www.24sevenbrinks.com/api/v1/gateway/static-report/deposits-statement-report"

    # payload = {
    #     'fecini': '2026/03/02',
    #     'fecfin': '2026/03/02'
    # }
    payload = {
        "renderType": 2,
        "initialDate": "2026-03-02T05:00:00.000Z",
        "endDate": "2026-03-02T05:00:00.000Z",
        "initialTime": "",
        "endTime": "",
        "countryId": "",
        "transporterId": "",
        "branchId": "",
        "customerName": "CONSUERTE",
        "contractCode": "",
        "depositType": "",
        "financialModality": ""
    }

    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    #     "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Content-Type": "application/x-www-form-urlencoded"
    # }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json"
    }


    # Usamos stream=True para descargas de archivos
    try:
        # Usamos la sesión para pedir el archivo
        response = session.post(url, json=payload, headers=headers, stream=True, timeout=30)
            # r.raise_for_status() # Lanza error si el status no es 200
        
        if response.status_code == 200:
            data_json = response.json()

            # 2. Extraer el contenido Base64
            contenido_base64 = data_json.get("content")

            if not contenido_base64:
                print("⚠️ El servidor respondió pero el campo 'content' está vacío.")
                return False
            
            # 3. Decodificar el Base64 a bytes reales
            archivo_bytes = base64.b64decode(contenido_base64)

            # 5. Guardar el archivo
            with open(nombre_archivo, "wb") as f:
                f.write(archivo_bytes)
            
            print(f"✅ Reporte de Brinks guardado en: {nombre_archivo}")
        else:
            print("elss")
            print(response.status_code)
            print(response.json())
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error de conexión: {e}")

session = iniciar_sesion_brinks()
print(session)
print("antes de descargar reporte")
descargar_reporte_brinks(session)
print("123")
# descargar_reporte(session)
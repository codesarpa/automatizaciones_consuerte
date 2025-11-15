from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
import os
import time

from playwright.sync_api import Page, expect
# from playwright import playwright 
from playwright.sync_api import sync_playwright
import re
import logging
import pandas as pd
from openpyxl import Workbook, load_workbook
import os
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage 
import smtplib

def enviar_correo(destinatario, mensaje, asunto):
    port = 465  # For SSL
    password = "ktgwqpeinquwykqq"
    remitente = "codesarpa.consuerte@gmail.com"

    # mensaje = "hola"

    email = EmailMessage() 
    email["From"] = remitente 
    email["To"] = destinatario 
    email["Subject"] = asunto

    email.set_content(mensaje, subtype="html") 
    smtp = smtplib.SMTP_SSL("smtp.gmail.com") 
    smtp.login(remitente, password) 
    smtp.sendmail(remitente, destinatario, email.as_string()) 
    smtp.quit()

class ManejadorImagenes(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        ruta = event.src_path
        archivo = os.path.basename(ruta)
        hora_actual = datetime.now()
        extension = os.path.splitext(archivo)[1].lower()

        # Validamos solo archivos PNG
        if extension != ".png":
            return

        print(f"Imagen detectada: {archivo}")

        # Obtenemos la fecha de referencia seg�n la hora
        if 0 <= hora_actual.hour < 3:
            # Madrugada (d�a anterior)
            fecha = (hora_actual - timedelta(days=1)).strftime("%d-%m-%Y")
            nombre_esperado = f"{fecha}.png"
        elif 0 <= hora_actual.hour < 14:
            # Entre 12 a.m. y 2 p.m.
            fecha = hora_actual.strftime("%d-%m-%Y")
            nombre_esperado = f"130_{fecha}.png"
        elif 15 <= hora_actual.hour < 17:
            # Entre 3 p.m. y 5 p.m.
            fecha = hora_actual.strftime("%d-%m-%Y")
            nombre_esperado = f"430_{fecha}.png"
        else:
            print("No es un horario válido para validar im�genes.")
            return

        # Validar si el nombre coincide
        if archivo == nombre_esperado:  # <- opcional si usas "_" en vez de "/"
            print("Imagen válida:", archivo)
            destinatario = "auxanalista@consuerte.com.co"
            mensaje = f"Se encontró la siguiente imagen en la compartida de escrutinio: {archivo}"
            asunto = "MONITOREO COMPARTIDA"
            enviar_correo(destinatario,mensaje,asunto)
        else:
            print("Imagen inválida.")
            print(f"Esperaba: {nombre_esperado}")
            print(f"Recibió: {archivo}")

# ---------------- CONFIGURACION ----------------
ruta_carpeta = r"//10.1.1.1/codesarpamoni/Escrutinio"  # <- c�mbiala por tu carpeta

observer = Observer()
observer.schedule(ManejadorImagenes(), ruta_carpeta, recursive=False)
observer.start()

print(f"Vigilando carpeta: {ruta_carpeta}")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    print("Monitoreo detenido.")
observer.join()

def enviar_imagenes():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    page = browser.new_page()
    page.goto("https://web.whatsapp.com/")

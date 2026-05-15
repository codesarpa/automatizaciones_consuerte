from dotenv import load_dotenv
import os
from datetime import datetime
import logging

# 📍 Directorio donde está este archivo (config.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔥 Carga DIRECTAMENTE el .env.production
load_dotenv(os.path.join(BASE_DIR, ".env.production"), override=True)

URL_SUPERFLEX = os.getenv("URL_SUPERFLEX")
ENVIRONMENT = os.getenv("ENVIRONMENT")
URL_HOME = os.getenv("URL_HOME")
URL_ADMIN_USUARIOS = os.getenv("URL_ADMIN_USUARIOS")
USER = os.getenv("USER")
PASS = os.getenv("PASS")
URL_USUARIOS_BODEGAS = os.getenv("URL_USUARIOS_BODEGAS")

def logs_diarios():
    ruta_base = os.path.dirname(__file__)
    fecha = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
    nombre_log = f"{fecha}.log"
    log_file = os.path.join(ruta_base, "logs", nombre_log)

    logging.basicConfig(
        filename=f'{log_file}',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    # print(log_file)
    logs = [
        logging.getLogger(__name__),
        log_file
    ]
    return logs
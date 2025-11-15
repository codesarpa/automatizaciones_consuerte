from dotenv import load_dotenv
import os
from datetime import datetime
import logging

# Carga el .env principal
load_dotenv()

env = os.getenv("PYTHON_ENV", "development")
env_files = {
    "development": ".env.development",
    "production": ".env.production"
}

# Carga las variables específicas del entorno activo
load_dotenv(env_files.get(env, ".env.development"))

URL_SUPERFLEX = os.getenv("URL_SUPERFLEX")
ENVIRONMENT = os.getenv("ENVIRONMENT")
URL_HOME = os.getenv("URL_HOME")
URL_ADMIN_USUARIOS = os.getenv("URL_ADMIN_USUARIOS")
USER = os.getenv("USER")
PASS = os.getenv("PASS")

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
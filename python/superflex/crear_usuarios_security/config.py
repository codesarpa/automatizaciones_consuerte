from dotenv import load_dotenv
import os

# Carga el .env principal
load_dotenv()

env = os.getenv("PYTHON_ENV", "development")
env_files = {
    "development": ".env.development",
    "production": ".env.production"
}

# Carga las variables específicas del entorno activo
load_dotenv(env_files.get(env, ".env.development"))

URL_SUPERFLEX_SECURITY = os.getenv("URL_SUPERFLEX_SECURITY")
ENVIRONMENT = os.getenv("ENVIRONMENT")
URL_HOME_SECURITY = os.getenv("URL_HOME_SECURITY")
URL_ADMIN_USUARIOS = os.getenv("URL_ADMIN_USUARIOS")
USER = os.getenv("USER")
PASS = os.getenv("PASS")
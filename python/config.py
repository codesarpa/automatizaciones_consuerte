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

URL_SUPERFLEX = os.getenv("URL_SUPERFLEX")
ENVIRONMENT = os.getenv("ENVIRONMENT")
URL_HOME = os.getenv("URL_HOME")
USER = os.getenv("USER")
PASS = os.getenv("PASS")
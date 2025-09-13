import os
from dotenv import load_dotenv

load_dotenv()

class DataStageConfig:
    """
    Configuración para la conexión a DataStage.
    Los valores se cargan desde variables de entorno o el archivo .env.
    """
    DOMAIN = os.getenv("DATASTAGE_DOMAIN")
    USER = os.getenv("DATASTAGE_USER")
    PASSWORD = os.getenv("DATASTAGE_PASSWORD")
    SERVER = os.getenv("DATASTAGE_SERVER")
    PROJECT = os.getenv("DATASTAGE_PROJECT")

# Instancia de configuración para fácil acceso
datastage_config = DataStageConfig()

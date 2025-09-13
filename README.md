# Servidor MCP de DataStage

Este proyecto implementa un Servidor de Protocolo de Contexto Modelo (MCP) en Python, utilizando la librería `FastMCP`, diseñado para interactuar de forma programática con IBM DataStage. Actúa como un puente que expone las funcionalidades de las herramientas de línea de comandos de DataStage (`dsjob`, `dsexport`, `dssearch`) a través de una interfaz web, facilitando la automatización, monitoreo y gestión de trabajos de DataStage.

## Características Principales

*   **Integración Robusta con DataStage:** Permite la ejecución de comandos nativos de DataStage (`dsjob`, `dsexport`, `dssearch`) directamente desde el servidor MCP.
*   **Interfaz Web (HTTP):** Proporciona un endpoint HTTP (`http://127.0.0.1:8000/mcp`) para la comunicación, lo que facilita la integración con Gemini CLI y otras aplicaciones o scripts externos.
*   **Arquitectura Extensible Basada en YAML:** Las herramientas de DataStage se definen y configuran mediante archivos YAML, permitiendo una fácil adición, modificación o eliminación de funcionalidades sin alterar el código base del servidor.
*   **Gestión de Configuración Centralizada:** Utiliza variables de entorno (cargadas desde un archivo `.env`) para gestionar de forma segura y flexible las credenciales y parámetros de conexión a DataStage.
*   **Mecanismo de Caché Inteligente:** Incorpora un sistema de caché basado en SQLite para almacenar temporalmente los resultados de comandos de DataStage, mejorando el rendimiento y reduciendo la carga en el servidor de DataStage para consultas repetitivas.
*   **Manejo de Errores Detallado:** Proporciona un manejo de errores específico para los comandos de DataStage, ofreciendo mensajes claros en caso de fallos de ejecución o configuración.

## Tecnologías Utilizadas

*   **Python 3.13+:** Lenguaje de programación principal.
*   **FastMCP:** Framework para la creación de servidores de Protocolo de Contexto Modelo.
*   **PyYAML:** Para la carga y parseo de archivos de configuración YAML.
*   **python-dotenv:** Para la gestión de variables de entorno.
*   **SQLite3:** Base de datos ligera utilizada para el sistema de caché.
*   **subprocess:** Módulo de Python para la ejecución de comandos externos (herramientas de DataStage).

## Estructura del Proyecto

```
.
├── .gitignore
├── README.md
├── mcp_client/
│   └── client.py          # Cliente de ejemplo para interactuar con el servidor MCP.
└── mcp_server/
    ├── .python-version    # Especifica la versión de Python utilizada (3.13).
    ├── discovery_request.json # Archivo de ejemplo para la solicitud de descubrimiento de MCP.
    ├── main.py            # Punto de entrada principal para iniciar el servidor MCP.
    ├── requirements.txt   # Dependencias de Python del servidor.
    ├── server_prueba.py   # Archivo de prueba o ejemplo para FastMCP.
    ├── servidor.py        # Lógica principal para la creación y configuración del servidor FastMCP, incluyendo la carga dinámica de herramientas.
    ├── herramientas/      # Directorio que contiene las definiciones de herramientas MCP en formato YAML.
    ├── prompts/           # Directorio para definiciones de prompts MCP (ej. example_prompt.yaml).
    └── utilidades/        # Módulos de utilidad para el servidor.
        ├── cache.py       # Implementación del sistema de caché basado en SQLite.
        ├── config.py      # Gestión de la configuración a través de variables de entorno.
        └── datastage.py   # Lógica para la ejecución de comandos de DataStage y funciones auxiliares.
```

## Instalación

Para configurar y ejecutar el servidor MCP, siga los siguientes pasos:

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/hreine/Data-Stage-MCP-Server-Utils.git
    cd Data-Stage-MCP-Server-Utils
    ```

2.  **Crear y Activar un Entorno Virtual:** (Altamente recomendado para aislar las dependencias del proyecto)
    ```bash
    python -m venv .venv
    # En Windows:
    .venv\Scripts\activate
    # En Linux/macOS:
    source .venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r mcp_server/requirements.txt
    ```

4.  **Disponibilidad de Herramientas de DataStage:**
    Es crucial que las herramientas de línea de comandos de IBM DataStage (`dsjob`, `dsexport`, `dssearch`) estén instaladas en el sistema donde se ejecuta el servidor MCP y que sean accesibles a través de la variable de entorno `PATH`.

## Configuración

El servidor MCP gestiona la configuración de conexión a DataStage a través de variables de entorno.

1.  **Crear un archivo `.env`:** En el directorio raíz del proyecto (`Data-Stage-MCP-Server-Utils/`), cree un archivo llamado `.env`.

2.  **Definir Variables de Entorno:** Agregue las siguientes variables al archivo `.env`, reemplazando los valores de ejemplo con la información de su entorno DataStage:

    ```dotenv
    DATASTAGE_DOMAIN=your_datastage_domain_or_ip:port
    DATASTAGE_USER=your_datastage_username
    DATASTAGE_PASSWORD=your_datastage_password
    DATASTAGE_SERVER=your_datastage_engine_server_name
    DATASTAGE_PROJECT=your_default_datastage_project_name
    ```

    *   `DATASTAGE_DOMAIN`: Dominio o dirección IP y puerto del servidor de servicios de DataStage.
    *   `DATASTAGE_USER`: Nombre de usuario para autenticarse en DataStage.
    *   `DATASTAGE_PASSWORD`: Contraseña del usuario de DataStage.
    *   `DATASTAGE_SERVER`: Nombre del servidor de motor de DataStage.
    *   `DATASTAGE_PROJECT`: Nombre del proyecto de DataStage por defecto.

## Ejecución del Servidor MCP

Para iniciar el servidor MCP, asegúrese de que su entorno virtual esté activado y ejecute el siguiente comando desde el directorio raíz del proyecto:

```bash
python mcp_server/main.py
```

El servidor se iniciará y escuchará las solicitudes HTTP en `http://127.0.0.1:8000/mcp`.

## Uso con Gemini CLI

Una vez que el servidor MCP esté en ejecución, Gemini CLI podrá detectar y utilizar las herramientas de DataStage expuestas. La interacción se realiza mediante llamadas a funciones que corresponden a las herramientas definidas en el directorio `herramientas/`.

### Ejemplos de Uso de Herramientas

A continuación, se presentan ejemplos de cómo se pueden invocar algunas de las herramientas de DataStage a través del servidor MCP:

*   **`get_projects()`:** Lista todos los proyectos disponibles en DataStage.
    ```python
    # Ejemplo de llamada (la sintaxis exacta puede variar ligeramente en Gemini CLI)
    # get_projects()
    ```

*   **`get_jobs(project="MyDataStageProject")`:** Obtiene una lista de todos los trabajos dentro de un proyecto específico de DataStage.
    ```python
    # get_jobs(project="CERT_FIDUCIARIA")
    ```

*   **`get_jobs_with_status(project="MyDataStageProject", status="96,97")`:** Lista los trabajos en un proyecto con estados de ejecución específicos (ej. `DSJS_CRASHED` o `DSJS_STOPPED`).
    ```python
    # get_jobs_with_status(project="CERT_FIDUCIARIA", status="96,97")
    ```

*   **`get_job_info(project="MyDataStageProject", job="MyJob")`:** Recupera información detallada sobre un trabajo específico.
    ```python
    # get_job_info(project="CERT_FIDUCIARIA", job="JOB_CLEAN_DS")
    ```

*   **`get_stages(project="MyDataStageProject", job="MyJob")`:** Lista todas las etapas (stages) de un trabajo de DataStage.
    ```python
    # get_stages(project="CERT_FIDUCIARIA", job="JOB_CLEAN_DS")
    ```

*   **`get_links(project="MyDataStageProject", job="MyJob", stage="MyStage")`:** Obtiene los enlaces asociados a una etapa específica dentro de un trabajo.
    ```python
    # get_links(project="CERT_FIDUCIARIA", job="JOB_CLEAN_DS", stage="RG_BORRADO")
    S```

*   **`get_params(project="MyDataStageProject", job="MyJob")`:** Lista los parámetros definidos para un trabajo de DataStage.
    ```python
    # get_params(project="CERT_FIDUCIARIA", job="JOB_CLEAN_DS")
    ```

*   **`export_job_to_file(object_name="MyJob", output_file="/path/to/MyJob.isx", project="MyDataStageProject")`:** Exporta un trabajo de DataStage a un archivo `.isx`.
    ```python
    # export_job_to_file(object_name="JOB_CLEAN_DS", output_file="/tmp/JOB_CLEAN_DS.isx", project="CERT_FIDUCIARIA")
    ```

*   **`dssearch_command(search_string="Customer", project="MyDataStageProject")`:** Busca objetos de DataStage que coincidan con una cadena de búsqueda.
    *   **Nota:** Esta función simula la búsqueda listando trabajos y filtrando por nombre, ya que `dssearch` no es una herramienta de línea de comandos estándar de DataStage.

## Contribución

Las contribuciones son bienvenidas y valoradas. Para contribuir a este proyecto, por favor siga los siguientes pasos:

1.  **Fork el Repositorio:** Cree un fork de este repositorio en su cuenta de GitHub.
2.  **Cree una Rama de Característica:**
    ```bash
    git checkout -b feature/nombre-de-su-caracteristica
    ```
3.  **Realice sus Cambios:** Implemente sus mejoras o correcciones.
4.  **Pruebe sus Cambios:** Asegúrese de que sus cambios funcionen correctamente y no introduzcan regresiones.
5.  **Commit sus Cambios:** Escriba un mensaje de commit claro y descriptivo.
    ```bash
    git commit -am 'feat: Añadir nueva funcionalidad X'
    ```
6.  **Suba su Rama:**
    ```bash
    git push origin feature/nombre-de-su-caracteristica
    ```
7.  **Abra un Pull Request:** Envíe un Pull Request a la rama `main` de este repositorio.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulte el archivo `LICENSE` en el repositorio para obtener más detalles.

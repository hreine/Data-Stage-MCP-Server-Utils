# Servidor MCP de DataStage

Este proyecto implementa un servidor de Protocolo de contexto modelo (MCP) basado en Python utilizando mcp[cli] para interactuar con IBM DataStage. Proporciona una interfaz web para ejecutar herramientas de línea de comandos de DataStage (`dsjob`, `dsexport`, y `dssearch`).

## Idioma

Español

## Estructura del Proyecto

```
mcp_server/
│
├── herramientas/          # Definiciones de herramientas MCP (dsjob.yaml, dsexport.yaml, dssearch.yaml)
├── utilidades/            # Lógica de comandos Data Stage reutilizable
│	└──datastage.py	   # Contiene la lógica para interactuar con las herramientas de línea de comandos de DataStage (`dsjob`, `dsexport`, `dssearch`) utilizando el módulo `subprocess` de Python.
├── servidor.py            # Crea el servidor MCP y registra las herramientas.
├── main.py                # Punto de entrada para el servidor MCP.
├── requirements.txt       # Enumera las dependencias de Python necesarias para ejecutar el servidor.
└── README.md              # Documentación del proyecto.
```

## Instalación

1.  **Clonar el repositorio** (si aún no lo has hecho):
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd mcp_server
    ```
2.  **Crear un entorno virtual** (recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # o
    .\venv\Scripts\activate   # En Windows
    ```
3.  **Instalar las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Asegúrate de que las herramientas de línea de comandos de DataStage estén disponibles**:
    Las herramientas `dsjob`, `dsexport` y `dssearch` (simulado) deben estar instaladas y accesibles en la variable de entorno `PATH` de tu sistema.

## Ejecución del Servidor MCP

Para iniciar el servidor MCP, ejecuta el siguiente comando desde el directorio `mcp_server/`:

```bash
python main.py
```

El servidor se iniciará y escuchará las solicitudes del Gemini CLI.

## Uso con Gemini CLI

Una vez que el servidor MCP esté en ejecución, Gemini CLI podrá detectar y utilizar las herramientas de DataStage expuestas.

### `dsjob`

Permite ejecutar comandos `dsjob` en DataStage.

**Ejemplo:** Ejecutar un trabajo de DataStage.
```
dsjob_command(project="MyProject", job_name="MyJob", command="run")
```

**Ejemplo:** Obtener el log de un trabajo.
```
dsjob_command(project="MyProject", job_name="MyJob", command="log")
```

### `dsexport`

Permite exportar objetos de DataStage.

**Ejemplo:** Exportar un trabajo de DataStage a un archivo.
```
dsexport_command(project="MyProject", object_type="JOB", object_name="MyJob", output_file="/path/to/MyJob.isx")
```

### `dssearch` (Simulado)

Permite buscar objetos en DataStage. Actualmente, esta función simula la búsqueda listando trabajos y filtrando por nombre.

**Ejemplo:** Buscar trabajos que contengan "Customer" en su nombre.
```
dssearch_command(project="MyProject", search_string="Customer")
```

## Configuración con Gemini CLI

Para asegurar que Gemini CLI pueda interactuar correctamente con el servidor MCP, sigue estos pasos:

1.  **Activar el entorno virtual**: Es crucial activar el entorno virtual donde se instalaron las dependencias del proyecto. Esto asegura que el intérprete de Python correcto y las librerías necesarias estén disponibles.
    ```bash
    .\venv\Scripts\activate   # En Windows
    # source venv/bin/activate  # En Linux/macOS
    ```

2.  **Ejecutar el servidor MCP**: Una vez activado el entorno virtual, inicia el servidor MCP. En Windows, es recomendable usar la siguiente sintaxis para asegurar la correcta codificación de caracteres en la consola:
    ```bash
    chcp 65001 && set PYTHONIOENCODING=utf-8 && python mcp_server/main.py &
    ```
    (El `&` al final ejecuta el servidor en segundo plano, permitiéndote seguir usando la terminal.)

    En Linux/macOS, puedes usar:
    ```bash
    python mcp_server/main.py &
    ```

Una vez que el servidor esté en ejecución, Gemini CLI podrá detectar y utilizar las herramientas de DataStage expuestas.

```

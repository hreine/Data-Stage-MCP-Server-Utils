import os
import yaml
import importlib
from fastmcp import FastMCP

# Importa el módulo datastage de utilidades.
# Esto es clave para que MCP pueda encontrar las funciones referenciadas
# en los archivos YAML (ej. 'datastage.dsjob_command').
from utilidades import datastage

def load_tools_from_directory(directory: str) -> list[dict]:
    tools_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                tool_config = yaml.safe_load(f)
                
                # Extract data from YAML
                name = tool_config["name"]
                description = tool_config["description"]
                function_path = tool_config["function"]

                # Dynamically import the function
                module_name, function_name = function_path.rsplit(".", 1)
                
                func = None
                if module_name == "datastage":
                    func = getattr(datastage, function_name)
                else:
                    # Fallback for other modules if they are added later
                    module = importlib.import_module(module_name)
                    func = getattr(module, function_name)

                if func:
                    tools_data.append({
                        "func": func,
                        "name": name,
                        "description": description,
                    })
    return tools_data


def load_prompts_from_directory(directory: str) -> dict:
    prompts_data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as f:
                prompt_config = yaml.safe_load(f)
                prompts_data[prompt_config["name"]] = prompt_config
    return prompts_data

def create_mcp_server():
    """
    Crea, configura y devuelve una instancia del servidor FastMCP para DataStage.

    Carga automáticamente todas las herramientas definidas en los archivos .yaml
    dentro del directorio 'herramientas'.
    """
    # 1. Crear una instancia del servidor MCP con un título descriptivo.
    mcp = FastMCP("Servidor MCP de DataStage", stateless_http=True, debug=True)

    # 2. Construir la ruta absoluta al directorio 'herramientas'.
    #    Esto asegura que el script funcione sin importar desde dónde se ejecute.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    herramientas_dir = os.path.join(base_dir, 'herramientas')

    # 3. Cargar todas las herramientas desde el directorio.
    tools_to_add = load_tools_from_directory(herramientas_dir)

    # 4. Registrar cada herramienta cargada en el servidor usando el decorador dinámicamente.
    for tool_data in tools_to_add:
        mcp.tool(name=tool_data["name"], description=tool_data["description"])(tool_data["func"])


    print(f"Servidor MCP '{mcp.name}' inicializado.")
    print(f"Se cargaron {len(tools_to_add)} herramientas desde '{herramientas_dir}':")
    for tool_data in tools_to_add:
        print(f"  - {tool_data['name']}")

    # 5. Construir la ruta absoluta al directorio 'prompts'.
    prompts_dir = os.path.join(base_dir, 'prompts')

    # 6. Cargar todos los prompts desde el directorio.
    prompts_loaded = load_prompts_from_directory(prompts_dir)

    print(f"Se cargaron {len(prompts_loaded)} prompts desde '{prompts_dir}':")
    for prompt_name in prompts_loaded:
        print(f"  - {prompt_name}")

    return mcp



"""Módulo principal del plugin de acceso rápido a URLs."""
import json
import os
import subprocess
import webbrowser
from pathlib import Path
import yaml

def load_aliases():
    """Carga los alias desde el archivo de configuración."""
    alias_file = Path(__file__).parent / "aliases.txt"
    aliases = {}

    if alias_file.exists():
        with open(alias_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line and "=" in line:
                    alias, url = line.split("=", 1)
                    aliases[alias.strip()] = url.strip()
    return aliases

def save_alias(alias, url):
    """Guarda un nuevo alias en el archivo de configuración."""
    alias_file = Path(__file__).parent / "aliases.txt"
    with open(alias_file, "a", encoding="utf-8") as file:
        file.write(f"\n{alias}={url}")

def edit_config():
    """Abre el archivo de configuración en el editor predeterminado."""
    alias_file = Path(__file__).parent / "aliases.txt"
    if not alias_file.exists():
        alias_file.touch()

    if os.name == 'nt':  # Windows
        os.startfile(alias_file)
    else:  # Unix
        subprocess.run(['xdg-open', str(alias_file)], check=True)

def execute(command, parent=None, **kwargs):  # pylint: disable=unused-argument
    """Ejecuta un comando."""
    parts = command.split(maxsplit=2)

    if len(parts) < 2:
        return

    alias = parts[1]
    url = parts[2] if len(parts) > 2 else None

    if alias == ".c":
        edit_config()
        return

    if alias == ".r":
        # La recarga se hace automáticamente en cada llamada a load_aliases()
        return

    aliases = load_aliases()

    if url:  # Modo guardar alias
        save_alias(alias, url)
    elif alias in aliases:  # Modo abrir URL
        webbrowser.open(aliases[alias], new=2)

def get_plugin_info():
    """Obtiene la información del plugin."""
    with open(os.path.join(os.path.dirname(__file__), "plugin.yaml"), "r", encoding="utf-8") as file:
        return json.dumps(yaml.safe_load(file))

def interact(feedback):
    """Interactúa con el usuario mostrando sugerencias de alias."""
    aliases = load_aliases()
    filtered_aliases = []

    if feedback:
        filtered_aliases = [
            alias for alias in aliases
            if alias.lower().startswith(feedback.lower())
        ]
        filtered_aliases.sort()

    message = filtered_aliases[0] if filtered_aliases else ""

    response = {
        "interaction": {
            "message": message,
            "placeholder": "Use '.c' para editar el archivo de configuración '.r' para recargarlo",
            "dropdown_items": filtered_aliases
        }
    }
    return json.dumps(response)

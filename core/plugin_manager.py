"""Módulo de gestión de plugins."""
import os
import importlib.util
import json
import functions as f

class PluginManager:
    """Clase de gestión de plugins."""
    def __init__(self, plugins_path, config):
        self.plugins_path = plugins_path
        self.plugins = {}
        self.config = config

    def load_plugins(self, parent=None):
        """Carga los plugins desde el directorio de plugins y verifica discrepancias con config.json."""
        config_plugins = self.config.get("plugins", {})
        directory_plugins = {}

        # Cargar plugins desde el directorio
        for plugin_name in os.listdir(self.plugins_path):
            plugin_dir = os.path.join(self.plugins_path, plugin_name)
            main_file = os.path.join(plugin_dir, "main.py")
            if os.path.isdir(plugin_dir) and os.path.isfile(main_file):
                spec = importlib.util.spec_from_file_location(f"plugins.{plugin_name}.main", main_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'get_plugin_info'):
                    plugin_info = module.get_plugin_info()
                    directory_plugins[plugin_name] = module
                    print(f"Loaded plugin: {plugin_name} with info: {plugin_info}")

        # Verificar discrepancias
        missing_in_directory = [plugin for plugin in config_plugins if plugin not in directory_plugins]
        missing_in_config = [plugin for plugin in directory_plugins if plugin not in config_plugins]

        if missing_in_directory or missing_in_config:
            error_message = "Discrepancias encontradas en los plugins:\n"
            if missing_in_directory:
                #modificar el mensaje de error para que si hay más de un elemento en missing_in_directory,
                # todos estén separados por comas excepto el penúltimo y el último que estarán separados por una "y"
                if len(missing_in_directory) > 1:
                    missing_str = f.local_join(missing_in_directory)
                else:
                    missing_str = missing_in_directory[0]
                error_message += f"Se ha{'n' if len(missing_in_directory) > 1 else ''} eliminado: {missing_str}\n"

                #eliminar plugins faltantes en el directorio del config
                for plugin in missing_in_directory:
                    del config_plugins[plugin]
                self.config["plugins"] = config_plugins
                f.save_json("config.json", self.config)

            if missing_in_config:
                #añadir plugins faltantes en el directorio al config
                for plugin in missing_in_config:
                    plugin_info = json.loads(directory_plugins[plugin].get_plugin_info())
                    config_plugins[plugin] = {"name":plugin_info["name"], "enabled":True, "keyword":plugin_info["default_keyword"]}
                self.config["plugins"] = config_plugins
                f.save_json("config.json", self.config)

                if len(missing_in_config) > 1:
                    missing_str = f.local_join(missing_in_config)
                else:
                    missing_str = missing_in_config[0]
                error_message += f"Se ha{'n' if len(missing_in_config) > 1 else ''} agregado: {missing_str}\n"

            f.notify(error_message, parent=parent, button_options={"accept": True})

        self.plugins = directory_plugins

    def get_plugin_info(self, plugin_name):
        """Obtiene la información de un plugin."""
        return self.plugins.get(plugin_name, None)

    def get_all_plugins_info(self):
        """Obtiene la información de todos los plugins."""
        return self.plugins

    def get_plugin_for_command(self, command):
        """Obtiene el nombre del plugin asociado a un comando."""
        for plugin_name, module in self.plugins.items():
            plugin_info = json.loads(module.get_plugin_info())
            default_keyword = plugin_info.get("plugin", {}).get("default_keyword")
            if command == self.config["plugins"].get(plugin_name, {}).get("keyword", default_keyword):
                return plugin_name
        return None

    def execute_plugin_command(self, plugin_name, command, **kwargs):
        """Ejecuta un comando de un plugin."""
        if plugin_name in self.plugins:
            module = self.plugins[plugin_name]
            module.execute(command, **kwargs)

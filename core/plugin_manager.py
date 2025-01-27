import os
import importlib.util

class PluginManager:
    def __init__(self, plugins_path):
        self.plugins_path = plugins_path
        self.plugins = {}

    def load_plugins(self):
        for plugin_name in os.listdir(self.plugins_path):
            plugin_dir = os.path.join(self.plugins_path, plugin_name)
            main_file = os.path.join(plugin_dir, "main.py")
            if os.path.isdir(plugin_dir) and os.path.isfile(main_file):
                spec = importlib.util.spec_from_file_location(f"plugins.{plugin_name}.main", main_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'get_plugin_info'):
                    plugin_info = module.get_plugin_info()
                    self.plugins[plugin_name] = plugin_info
                    print(f"Loaded plugin: {plugin_name} with info: {plugin_info}")

    def get_plugin_info(self, plugin_name):
        return self.plugins.get(plugin_name, None)

    def get_all_plugins_info(self):
        return self.plugins
import os
import importlib.util

class PluginManager:
    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir
        self.plugins = []

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py'):
                self.load_plugin(filename)

    def load_plugin(self, filename):
        plugin_path = os.path.join(self.plugin_dir, filename)
        spec = importlib.util.spec_from_file_location(filename, plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.plugins.append(module)

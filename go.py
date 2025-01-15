import json
import os
import subprocess
import webbrowser
from notification import Notification

class GoModule:
    def __init__(self, parent):
        self.parent = parent
        self.go_data = self.loadGoData()

    def loadGoData(self):
        if os.path.exists("go.json"):
            with open("go.json", "r") as file:
                return json.load(file)
        return {}

    def saveGoData(self):
        with open("go.json", "w") as file:
            json.dump(self.go_data, file, indent=4)

    def handleGoCommand(self, command):
        if command.startswith("add "):
            parts = command[4:].split(" ")
            if len(parts) == 2 and parts[0].startswith("[") and parts[0].endswith("]") and parts[1].startswith("(") and parts[1].endswith(")"):
                alias = parts[0][1:-1]
                url = parts[1][1:-1]
                self.go_data[alias] = url
                self.saveGoData()
                return f"Alias '{alias}' agregado con URL '{url}'"
            else:
                return "Formato incorrecto. Use 'go add [alias] (url)'"
        else:
            return self.filterDropdownItems(command)

    def filterDropdownItems(self, filter_text):
        """Filtra los elementos del desplegable que concuerden con el texto del filtro."""
        self.parent.dropdown.clear()
        if self.go_data:
            for alias, url in self.go_data.items():
                if filter_text.lower() in alias.lower():
                    self.parent.dropdown.addItem(f"{alias}\n{url}")
            if not self.parent.dropdown.items:
                self.parent.dropdown.addItem(f"No se encontró el alias '{filter_text}'. Use 'go add [{filter_text}] (url)' para crearlo.")
        else:
            self.parent.dropdown.addItem("No existen alias, cree uno con 'go add [alias] (url)'")

    def executeGoCommand(self, alias):
        if alias in self.go_data:
            url = self.go_data[alias]
            try:
                print(f"Ejecutando comando: webbrowser.open({url})")
                webbrowser.open(url, new=0, autoraise=True)
                notification = Notification(f"Abriendo {url}", 3000, self.parent)
                notification.showNotification()
                self.parent.hideWidget()
            except Exception as e:
                print(f"Error al abrir '{url}': {e}")
        else:
            if self.parent.dropdown.items and "No se encontró el alias" not in self.parent.dropdown.items[0].layout().itemAt(0).widget().text():
                alias = self.parent.getSelectedAlias()
                url = self.go_data[alias]
                try:
                    print(f"Ejecutando comando: webbrowser.open({url})")
                    webbrowser.open(url, new=0, autoraise=True)
                    notification = Notification(f"Abriendo {url}", 3000, self.parent)
                    notification.showNotification()
                    self.parent.hideWidget()
                except Exception as e:
                    print(f"Error al abrir '{url}': {e}")
            else:
                print(f"No se encontró el alias '{alias}'")

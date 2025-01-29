"""Módulo para manejar atajos de teclado y acciones"""
import logging
import keyboard

# Configuración del logger
logging.basicConfig(level=logging.INFO)
console = logging.getLogger(__name__)

class Action:
    """Clase para representar una acción"""
    def __init__(self, name, action):
        self.name = name
        self.action = action

    def __call__(self):
        if callable(self.action):
            self.action()
        else:
            raise TypeError(f"La acción {self.name} no es callable")

class Shortcut:
    """Clase para representar un atajo de teclado"""
    def __init__(self, hotkey_str):
        self.hotkey_str = hotkey_str

actions = {}
ids = {}

def add_hotkey_action(shortcut, action):
    """Agregar una acción de atajo de teclado"""
    if not callable(action):
        raise TypeError(f"La acción {action.name} no es callable")

    if shortcut.hotkey_str in actions and actions[shortcut.hotkey_str]:
        console.warning("El atajo %s ya está registrado", shortcut.hotkey_str)

    if shortcut.hotkey_str not in actions:
        actions[shortcut.hotkey_str] = []

    actions[shortcut.hotkey_str].append(action)

    if len(actions[shortcut.hotkey_str]) == 1:
        if shortcut.hotkey_str not in ids:
            ids[shortcut.hotkey_str] = len(ids)

        try:
            if callable(action.action):
                keyboard.add_hotkey(shortcut.hotkey_str, action.action)
                console.info("El atajo %s ha sido registrado", shortcut.hotkey_str)
                return True
            else:
                console.warning("La acción para %s no es callable", shortcut.hotkey_str)
                return False
        except ValueError as e:
            console.warning("No se pudo agregar el atajo %s. Excepción: %s", shortcut.hotkey_str, str(e))
            return False

    return True

def unregister_hotkeys_for_module(module_name):
    """Desregistrar atajos de teclado para un módulo"""
    for hotkey_str, action_list in list(actions.items()):
        action_list[:] = [a for a in action_list if a.module_name != module_name]

        if not action_list:
            try:
                keyboard.remove_hotkey(hotkey_str)
                console.info("El atajo %s ha sido desregistrado", hotkey_str)
            except ValueError as e:
                console.warning("No se pudo desregistrar el atajo %s. %s", hotkey_str, str(e))
            del actions[hotkey_str]

def populate_hotkey(shortcut):
    """Ejecutar la acción del atajo de teclado"""
    if actions:
        try:
            actions[shortcut.hotkey_str][0].action()
        except ValueError as ex:
            console.error("No se pudo ejecutar la acción del atajo de teclado. %s", str(ex))

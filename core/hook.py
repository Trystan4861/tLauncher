"""Module to handle hotkeys and actions"""
import logging
import keyboard

# Configuración del logger
logging.basicConfig(level=logging.INFO)
console = logging.getLogger(__name__)

class Shortcut:
    """Class to represent a hotkey"""
    def __init__(self, hotkey_str):
        self.hotkey_str = hotkey_str

class Action:
    """Class to represent an action"""
    def __init__(self, module_name, action):
        self.module_name = module_name
        self.action = action

actions = {}
ids = {}

def add_hotkey_action(shortcut, action):
    """Add a hotkey action"""
    if shortcut.hotkey_str in actions and actions[shortcut.hotkey_str]:
        console.warning("%s shortcut is already registered",shortcut.hotkey_str)

    if shortcut.hotkey_str not in actions:
        actions[shortcut.hotkey_str] = []

    actions[shortcut.hotkey_str].append(action)

    if len(actions[shortcut.hotkey_str]) == 1:
        if shortcut.hotkey_str not in ids:
            ids[shortcut.hotkey_str] = len(ids)

        try:
            keyboard.add_hotkey(shortcut.hotkey_str, action.action())
            console.info("%s shortcut registered",shortcut.hotkey_str)
            return True
        except ValueError as e:
            console.warning("Failed to add %s shortcut. Exception: %s", shortcut.hotkey_str, str(e))
            return False

    return True

def unregister_hotkeys_for_module(module_name):
    """Unregister hotkeys for a module"""
    for hotkey_str, action_list in list(actions.items()):
        action_list[:] = [a for a in action_list if a.module_name != module_name]

        if not action_list:
            try:
                keyboard.remove_hotkey(hotkey_str)
                console.info("%s shortcut unregistered",hotkey_str)
            except ValueError as e:
                console.warning("Failed to unregister %s shortcut. %s",hotkey_str, str(e))
            del actions[hotkey_str]

def populate_hotkey(shortcut):
    """Populate hotkey"""
    if actions:
        try:
            actions[shortcut.hotkey_str][0].action()
        except ValueError as ex:
            console.error("Failed to execute hotkey's action. %s", str(ex))

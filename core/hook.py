import keyboard
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
console = logging.getLogger(__name__)

class Shortcut:
    def __init__(self, hotkey_str):
        self.hotkey_str = hotkey_str

class Action:
    def __init__(self, moduleName, action):
        self.moduleName = moduleName
        self.action = action

actions = {}
ids = {}
runnerWindow = None

def add_hotkey_action(shortcut, action):
    if shortcut.hotkey_str in actions and actions[shortcut.hotkey_str]:
        console.warning(f"{shortcut.hotkey_str} shortcut is already registered")
    
    if shortcut.hotkey_str not in actions:
        actions[shortcut.hotkey_str] = []
    
    actions[shortcut.hotkey_str].append(action)
    
    if len(actions[shortcut.hotkey_str]) == 1:
        if shortcut.hotkey_str not in ids:
            ids[shortcut.hotkey_str] = len(ids)
        
        try:
            keyboard.add_hotkey(shortcut.hotkey_str, lambda: action.action())
            console.info(f"{shortcut.hotkey_str} shortcut registered")
            return True
        except Exception as e:
            console.warning(f"Failed to add {shortcut.hotkey_str} shortcut. Exception: {str(e)}")
            return False
    
    return True

def unregister_hotkeys_for_module(moduleName):
    for hotkey_str, action_list in list(actions.items()):
        action_list[:] = [a for a in action_list if a.moduleName != moduleName]
        
        if not action_list:
            try:
                keyboard.remove_hotkey(hotkey_str)
                console.info(f"{hotkey_str} shortcut unregistered")
            except Exception as e:
                console.warning(f"Failed to unregister {hotkey_str} shortcut. {str(e)}")
            del actions[hotkey_str]

def populate_hotkey(shortcut):
    if actions:
        try:
            actions[shortcut.hotkey_str][0].action()
        except Exception as ex:
            console.error(f"Failed to execute hotkey's action. {str(ex)}")
            
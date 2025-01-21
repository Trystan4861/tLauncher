import json

# JSON de ejemplo para el plugin
PLUGIN_INFO_TEMPLATE = {
    "plugin": {
        "name": "SamplePlugin",
        "description": "Muestra un mensaje de prueba.",
        "default_keyword": "say"
    }
}

PLUGIN_INTERACT_TEMPLATE = {
    "interaction": {
        "message": "Mensaje de prueba",
        "placeholder": "Placeholder",
        "dropdown_items": [
            {
                "caption1": "caption1.1",
                "caption2": "caption1.2",
                "visible": True,
                "buttons": [
                    {
                        "icon_file": "icon1.png",
                        "caption": "Botón 1",
                        "tooltip": "Tooltip del botón 1",
                        "index": 0,
                        "command": "command1",
                        "visible": False
                    },
                    {
                        "icon_file": "icon2.png",
                        "caption": "Botón 2",
                        "tooltip": "Tooltip del botón 2",
                        "index": 1,
                        "command": "command2",
                        "visible": False
                    }
                ]
            },
            {
                "caption1": "caption2.1",
                "caption2": "caption2.2",
                "visible": False,
                "buttons": [
                    {
                        "icon_file": "icon3.png",
                        "caption": "Botón 1",
                        "tooltip": "Tooltip del botón 1",
                        "index": 0,
                        "command": "command3",
                        "visible": False
                    }
                ]
            }
            # Puedes agregar más elementos aquí
        ]
    }
}

def execute(command):
    print(f"{command} from sample plugin!")

def get_plugin_info():
    return json.dumps(PLUGIN_INFO_TEMPLATE)

def interact(feedback):
    response = PLUGIN_INTERACT_TEMPLATE.copy()
    response["interaction"]["message"] = f"Received feedback: {feedback}"
    return json.dumps(response)

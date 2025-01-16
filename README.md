# tLauncher

tLauncher es una aplicación que permite ejecutar comandos de forma rápida y sencilla en Windows. Es una alternativa a ulauncher, diseñada específicamente para el sistema operativo Windows.

## Características

- **Interfaz translúcida**: Una interfaz de usuario moderna y minimalista.
- **Desplegable avanzado**: Un menú desplegable con funcionalidades avanzadas.
- **Icono en la bandeja del sistema**: Acceso rápido desde la bandeja del sistema.
- **Soporte para múltiples instancias**: Asegura que solo una instancia del programa esté en ejecución.
- **Estilos personalizables**: Personaliza la apariencia mediante archivos QSS.

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu_usuario/tLauncher.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd tLauncher
    ```
3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para ejecutar la aplicación, usa el siguiente comando:
```bash
python main.py
```

## Compilación

Para compilar la aplicación en un ejecutable, puedes usar `PyInstaller`. Sigue estos pasos:

1. Instala PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2. Compila la aplicación:
    ```bash
    pyinstaller --onefile --windowed main.py
    ```
3. El ejecutable se generará en el directorio `dist`.

## Archivos Principales

- `main.py`: Punto de entrada de la aplicación.
- `widget.py`: Implementación del widget translúcido.
- `dropdown.py`: Implementación del menú desplegable.
- `tray.py`: Implementación del icono en la bandeja del sistema.
- `styles.qss`: Archivo de estilos para la aplicación.
- `settings-icon.svg`: Icono de configuración utilizado en la interfaz.

# Changelog

## v1.1.17
- Añadida funcionalidad para eliminar un alias de `go` usando el comando `go delete [alias]`.
- Procesar la pulsación de teclas `Alt+[1-9]` para seleccionar elementos del desplegable.

## v1.1.16
- Actualizar configuración para reflejar cambios en la funcionalidad de la aplicación sin reiniciar.

## v1.1.15
- Modificado el comportamiento para ocultar la aplicación en lugar de cerrarla al abrir una URL.
- Revisado `notification.py` para asegurarse de que no propague el cierre a la aplicación principal.

## v1.1.14
- Extraída la funcionalidad del módulo "go" a un archivo aparte `go.py`.

## v1.1.13
- Mejoras en el módulo `go` para usar el alias del elemento seleccionado en el desplegable si el alias no existe.

## v1.1.12
- Añadidas instrucciones de compilación al archivo `README.md`.

## v1.1.11
- Solucionado el problema de que el input no recibía el foco automáticamente al mostrar el widget.

## v1.1.10
- Migrada la lógica del `trayIcon` y el menú contextual a un nuevo archivo `tray.py`.

## v1.1.9
- Corregido el error de `QCursor` no definido en `widget.py`.

## v1.1.8
- Modificado `main.py` para usar `widget.showWidget()` y asegurar que el input reciba el foco incluso en la primera vez que se muestra la primera instancia.

## v1.1.7
- Reemplazadas todas las llamadas a `self.show()` por `self.showWidget()`.

## v1.1.6
- Añadidas funciones `showWidget` y `hideWidget` para mostrar y ocultar el widget, asegurando que el input reciba el foco al mostrar el widget.

## v1.1.5
- Añadido icono en la barra de notificaciones
- Modificación del comportamiento para permitir sólo una instancia del programa en todo momento

## v1.1.4
- Corrección de estilos y tamaños en el desplegable:
  - Eliminación de la barra horizontal.
  - Ajuste del ancho del desplegable para coincidir con el input.
  - Fondo y texto del desplegable ajustados para contraste.

## v1.1.3
- Se ajustó el comportamiento del input para evitar pérdida de foco al interactuar con el desplegable.

## v1.1.2
- Estilo del desplegable actualizado para coincidir con el widget principal.
- Tamaño dinámico del desplegable basado en el número de elementos (máximo 5).

## v1.1.1
- El desplegable ahora es independiente del fondo del widget y no afecta su tamaño.

## v1.1.0
- División del código en tres archivos principales (`main.py`, `translucent_widget.py`, `dropdown.py`).
- Nueva función para modificar un elemento del desplegable por índice.
- Texto del input actualiza dinámicamente el elemento 1 del desplegable.
- Si el input está vacío, el desplegable se oculta automáticamente.

## v1.0.6
- Corrección del cierre del programa al perder el foco utilizando un monitor global de foco.

## v1.0.5
- La ventana ahora se posiciona automáticamente en el monitor 1 o centrada en la pantalla activa.

## v1.0.4
- Se agregó la funcionalidad de cierre automático al perder el foco.

## v1.0.3
- Aumento del tamaño del cuadro de texto a 55px de alto.
- Agregado un desplegable oculto debajo del cuadro de texto con funciones para agregar y eliminar elementos.
- Manejo de clics en elementos del desplegable.

## v1.0.2
- Ajuste del tamaño del widget a 450x120 y del cuadro de texto a 420x50.

## v1.0.1
- Cambio del botón para mostrar un icono y tamaño ajustado.
- Cuadro de texto central agregado.
- Respuesta a teclas ESC y ENTER implementada.
- Configuración inicial para enfoque al cuadro de texto.

## v1.0.0
- Creación inicial del widget translúcido con cierre.

# Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

# Autores

- [Trystan4861](https://github.com/trystan4861)

# Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

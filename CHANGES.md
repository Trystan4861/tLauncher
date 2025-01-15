# Changelog

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

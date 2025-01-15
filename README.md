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

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que desees realizar.

## Autor

- [Trystan4861](https://github.com/trystan4861)

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

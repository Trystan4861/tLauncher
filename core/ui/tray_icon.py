import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

class TrayIcon:
    def __init__(self, main_window):
        self.main_window = main_window
        self.icon = pystray.Icon("tLauncher")
        self.icon.menu = pystray.Menu(
            item('Show', self.show),
            item('Quit', self.quit)
        )
        self.icon.icon = self.create_image()

    def create_image(self):
        # Crear un icono simple para la bandeja de notificación
        image = Image.new('RGB', (64, 64), (255, 255, 255))
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            (0, 0, 64, 64),
            fill=(255, 0, 0),
            outline=(0, 0, 0)
        )
        return image

    def show(self, icon, item):
        self.main_window.show()

    def quit(self, icon, item):
        self.icon.stop()
        self.main_window.root.quit()

    def run(self):
        self.icon.run()

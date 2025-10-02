import pystray
from PIL import Image, ImageDraw
from typiDesk import TypiDesk, Config
from gui import SettingsWindow
import customtkinter

class TypiDeskApp:
    def __init__(self):
        self.config = Config()
        self.engine = TypiDesk(self.config)
        self.settings_window = None

        # Create a simple icon
        width = 64
        height = 64
        color1 = "#4A85E5"
        color2 = "#FFFFFF"
        image = Image.new("RGB", (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.text((10, 20), "TD", fill=color2, font_size=32)
        self.icon = image

    def run(self):
        self.engine.start()
        menu = pystray.Menu(
            pystray.MenuItem("TypiDesk", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Pause/Resume", self.toggle_pause),
            pystray.MenuItem("Settings", self.show_settings),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_app),
        )
        tray_icon = pystray.Icon("TypiDesk", self.icon, "TypiDesk", menu)
        tray_icon.run()

    def toggle_pause(self):
        if self.engine.listener and self.engine.listener.running:
            self.engine.pause()
        else:
            self.engine.start()

    def show_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self.config)
        else:
            self.settings_window.focus()

    def quit_app(self):
        self.engine.stop()
        if self.settings_window:
            self.settings_window.destroy()
        pystray.Icon.stop(self)

if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")
    app = TypiDeskApp()
    app.run()

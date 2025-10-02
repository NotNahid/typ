import customtkinter
from pynput import keyboard

class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.title("TypiDesk Settings")
        self.geometry("400x400")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- AI Model Setting ---
        self.model_label = customtkinter.CTkLabel(self, text="AI Model:")
        self.model_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.model_var = customtkinter.StringVar(value=self.config.GEMINI_MODEL)
        self.model_menu = customtkinter.CTkOptionMenu(
            self, values=["gemini-1.5-flash", "gemini-2.5-pro"], variable=self.model_var
        )
        self.model_menu.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")

        # --- Activation Key Setting ---
        self.activation_key_label = customtkinter.CTkLabel(self, text="Activation Key:")
        self.activation_key_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        key_map = {"Space": keyboard.Key.space, "Enter": keyboard.Key.enter}
        self.activation_key_var = customtkinter.StringVar(
            value=[k for k, v in key_map.items() if v == self.config.ACTIVATION_KEY][0]
        )
        self.activation_key_menu = customtkinter.CTkOptionMenu(
            self, values=list(key_map.keys()), variable=self.activation_key_var
        )
        self.activation_key_menu.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        # --- Save Button ---
        self.save_button = customtkinter.CTkButton(self, text="Save", command=self.save_settings)
        self.save_button.grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")

    def save_settings(self):
        self.config.GEMINI_MODEL = self.model_var.get()
        
        key_map = {"Space": keyboard.Key.space, "Enter": keyboard.Key.enter}
        self.config.ACTIVATION_KEY = key_map[self.activation_key_var.get()]
        
        print("Settings saved!")
        self.destroy()
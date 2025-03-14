import tkinter as tk
from tkinter import ttk
import keyboard
import time
import threading
import sys


class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Typer")
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        # Variables
        self.running = False
        self.letter_var = tk.StringVar(value="a")
        self.delay_var = tk.StringVar(value="0.1")
        self.status_var = tk.StringVar(value="Ready")
        self.hotkey_toggle = "f12"

        # Create tab control
        self.tab_control = ttk.Notebook(root)

        # Create single tab
        self.tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab, text='Auto Typer')
        self.tab_control.pack(expand=1, fill="both")

        # Create content in tab
        self.create_widgets()

        # Setup keyboard hook for toggle
        keyboard.add_hotkey(self.hotkey_toggle, self.toggle_typing)

        # When closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Letter input
        ttk.Label(self.tab, text="Letter/Text to Type:").pack(pady=(20, 5))
        ttk.Entry(self.tab, textvariable=self.letter_var, width=20).pack()

        # Delay input
        ttk.Label(self.tab, text="Delay (seconds):").pack(pady=(10, 5))
        ttk.Entry(self.tab, textvariable=self.delay_var, width=20).pack()

        # Toggle button
        ttk.Button(self.tab, text="Toggle (F12)", command=self.toggle_typing).pack(pady=15)

        # Status
        ttk.Label(self.tab, textvariable=self.status_var, foreground="blue").pack(pady=10)

        # Instructions
        instructions = "Press F12 to start/stop typing\n(Works even when this window is not focused)"
        ttk.Label(self.tab, text=instructions, foreground="gray").pack(pady=5)

    def typing_thread(self):
        try:
            delay = float(self.delay_var.get())
        except ValueError:
            delay = 0.1
            self.delay_var.set("0.1")

        text_to_type = self.letter_var.get()
        if not text_to_type:
            text_to_type = "a"
            self.letter_var.set("a")

        self.status_var.set("Running...")

        while self.running:
            if self.running:  # Double-check to prevent race condition
                keyboard.write(text_to_type)
                time.sleep(delay)

    def toggle_typing(self):
        if self.running:
            # Stop typing
            self.running = False
            self.status_var.set("Stopped")
        else:
            # Start typing
            self.running = True
            threading.Thread(target=self.typing_thread, daemon=True).start()

    def on_close(self):
        self.running = False
        keyboard.unhook_all()
        self.root.destroy()
        sys.exit(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import pyautogui
import json
import keyboard
import os


class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Auto Clicker")
        self.root.geometry("600x800")

        # Default settings
        self.settings = {
            "cps": 10,  # Changed from "click_interval": 0.1
            "randomize_interval": False,
            "random_min": 0.1,
            "random_max": 0.5,
            "mouse_button": "left",
            "click_type": "single",
            "position_type": "current",
            "position_x": 0,
            "position_y": 0,
            "click_count": 0,
            "start_delay": 0,
            "hotkey": "f6"
        }

        self.load_settings()

        # Initialize variables
        self.clicking = False
        self.click_thread = None

        # Create GUI
        self.create_gui()

        # Configure hotkey
        self.setup_hotkey()

        # Make window stay on top
        self.root.attributes("-topmost", True)

        # Handle close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_gui(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill="both", expand=True)

        # Status frame
        status_frame = ttk.LabelFrame(self.main_frame, text="Status")
        status_frame.pack(fill="x", padx=10, pady=10)

        # Status label
        self.status_label = ttk.Label(status_frame, text="Ready", font=("Arial", 14))
        self.status_label.pack(padx=10, pady=10)

        # Hotkey display
        hotkey_frame = ttk.Frame(status_frame)
        hotkey_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(hotkey_frame, text="Toggle Hotkey:").pack(side="left", padx=(0, 5))
        self.hotkey_label = ttk.Label(hotkey_frame, text=self.settings["hotkey"].upper())
        self.hotkey_label.pack(side="left")

        ttk.Button(hotkey_frame, text="Change", command=self.change_hotkey).pack(side="right")

        # Clicking options
        click_frame = ttk.LabelFrame(self.main_frame, text="Clicking Options")
        click_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(click_frame, text="Clicks Per Second (CPS):").grid(column=0, row=0, padx=10, pady=10, sticky="w")
        self.cps_var = tk.DoubleVar(value=self.settings["cps"])
        cps_entry = ttk.Entry(click_frame, textvariable=self.cps_var)
        cps_entry.grid(column=1, row=0, padx=10, pady=10)

        self.randomize_var = tk.BooleanVar(value=self.settings["randomize_interval"])
        randomize_check = ttk.Checkbutton(click_frame, text="Randomize Interval", variable=self.randomize_var)
        randomize_check.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky="w")

        random_frame = ttk.Frame(click_frame)
        random_frame.grid(column=0, row=2, columnspan=2, padx=10, pady=10, sticky="w")

        ttk.Label(random_frame, text="Random Min:").pack(side="left", padx=(0, 5))
        self.random_min_var = tk.DoubleVar(value=self.settings["random_min"])
        random_min_entry = ttk.Entry(random_frame, textvariable=self.random_min_var, width=5)
        random_min_entry.pack(side="left", padx=(0, 10))

        ttk.Label(random_frame, text="Random Max:").pack(side="left", padx=(0, 5))
        self.random_max_var = tk.DoubleVar(value=self.settings["random_max"])
        random_max_entry = ttk.Entry(random_frame, textvariable=self.random_max_var, width=5)
        random_max_entry.pack(side="left")

        # Mouse button options
        mouse_frame = ttk.LabelFrame(self.main_frame, text="Mouse Button")
        mouse_frame.pack(fill="x", padx=10, pady=10)

        self.mouse_button_var = tk.StringVar(value=self.settings["mouse_button"])
        ttk.Radiobutton(mouse_frame, text="Left Click", value="left", variable=self.mouse_button_var).grid(column=0,
                                                                                                           row=0,
                                                                                                           padx=10,
                                                                                                           pady=5,
                                                                                                           sticky="w")
        ttk.Radiobutton(mouse_frame, text="Middle Click", value="middle", variable=self.mouse_button_var).grid(column=0,
                                                                                                               row=1,
                                                                                                               padx=10,
                                                                                                               pady=5,
                                                                                                               sticky="w")
        ttk.Radiobutton(mouse_frame, text="Right Click", value="right", variable=self.mouse_button_var).grid(column=0,
                                                                                                             row=2,
                                                                                                             padx=10,
                                                                                                             pady=5,
                                                                                                             sticky="w")

        # Click type
        click_type_frame = ttk.LabelFrame(self.main_frame, text="Click Type")
        click_type_frame.pack(fill="x", padx=10, pady=10)

        self.click_type_var = tk.StringVar(value=self.settings["click_type"])
        ttk.Radiobutton(click_type_frame, text="Single Click", value="single", variable=self.click_type_var).grid(
            column=0, row=0, padx=10, pady=5, sticky="w")
        ttk.Radiobutton(click_type_frame, text="Double Click", value="double", variable=self.click_type_var).grid(
            column=1, row=0, padx=10, pady=5, sticky="w")

        # Position options
        position_frame = ttk.LabelFrame(self.main_frame, text="Click Position")
        position_frame.pack(fill="x", padx=10, pady=10)

        self.position_var = tk.StringVar(value=self.settings["position_type"])
        ttk.Radiobutton(position_frame, text="Current Mouse Position", value="current",
                        variable=self.position_var).grid(column=0, row=0, columnspan=2, padx=10, pady=5, sticky="w")
        ttk.Radiobutton(position_frame, text="Custom Position", value="custom", variable=self.position_var).grid(
            column=0, row=1, columnspan=2, padx=10, pady=5, sticky="w")

        position_entry_frame = ttk.Frame(position_frame)
        position_entry_frame.grid(column=0, row=2, columnspan=2, padx=10, pady=5, sticky="w")

        ttk.Label(position_entry_frame, text="X:").pack(side="left", padx=(0, 5))
        self.position_x_var = tk.IntVar(value=self.settings["position_x"])
        position_x_entry = ttk.Entry(position_entry_frame, textvariable=self.position_x_var, width=5)
        position_x_entry.pack(side="left", padx=(0, 10))

        ttk.Label(position_entry_frame, text="Y:").pack(side="left", padx=(0, 5))
        self.position_y_var = tk.IntVar(value=self.settings["position_y"])
        position_y_entry = ttk.Entry(position_entry_frame, textvariable=self.position_y_var, width=5)
        position_y_entry.pack(side="left", padx=(0, 10))

        ttk.Button(position_entry_frame, text="Get Current Position", command=self.get_current_position).pack(
            side="left")

        # Additional options
        additional_frame = ttk.LabelFrame(self.main_frame, text="Additional Options")
        additional_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(additional_frame, text="Start Delay (seconds):").grid(column=0, row=0, padx=10, pady=5, sticky="w")
        self.start_delay_var = tk.DoubleVar(value=self.settings["start_delay"])
        start_delay_entry = ttk.Entry(additional_frame, textvariable=self.start_delay_var, width=5)
        start_delay_entry.grid(column=1, row=0, padx=10, pady=5, sticky="w")

        ttk.Label(additional_frame, text="Click Count (0 = infinite):").grid(column=0, row=1, padx=10, pady=5,
                                                                             sticky="w")
        self.click_count_var = tk.IntVar(value=self.settings["click_count"])
        click_count_entry = ttk.Entry(additional_frame, textvariable=self.click_count_var, width=5)
        click_count_entry.grid(column=1, row=1, padx=10, pady=5, sticky="w")

        # Control buttons
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill="x", padx=10, pady=20)

        start_button = ttk.Button(control_frame, text="Start (F6)", command=self.start_clicking)
        start_button.pack(side="left", padx=5, expand=True, fill="x")

        stop_button = ttk.Button(control_frame, text="Stop (F6)", command=self.stop_clicking)
        stop_button.pack(side="right", padx=5, expand=True, fill="x")

    def start_clicking(self):
        if not self.clicking:
            self.clicking = True
            self.status_label.config(text="Clicking...")

            # Save settings
            self.settings.update({
                "cps": self.cps_var.get(),  # Changed from click_interval
                "randomize_interval": self.randomize_var.get(),
                "random_min": self.random_min_var.get(),
                "random_max": self.random_max_var.get(),
                "mouse_button": self.mouse_button_var.get(),
                "click_type": self.click_type_var.get(),
                "position_type": self.position_var.get(),
                "position_x": self.position_x_var.get(),
                "position_y": self.position_y_var.get(),
                "click_count": self.click_count_var.get(),
                "start_delay": self.start_delay_var.get()
            })

            # Start clicking in a separate thread
            self.click_thread = threading.Thread(target=self.auto_click)
            self.click_thread.daemon = True
            self.click_thread.start()

    def stop_clicking(self):
        if self.clicking:
            self.clicking = False
            self.status_label.config(text="Stopped")

            # Wait for thread to finish if it's running
            if self.click_thread and self.click_thread.is_alive():
                self.click_thread.join(0.5)
                self.click_thread = None

    def auto_click(self):
        if self.start_delay_var.get() > 0:
            time.sleep(self.start_delay_var.get())

        click_count = self.click_count_var.get()

        while self.clicking and (click_count == 0 or click_count > 0):
            # Handle different click types
            if self.click_type_var.get() == "double":
                clicks = 2
            else:
                clicks = 1

            # Perform the click at specified position or current position
            if self.position_var.get() == "custom":
                pyautogui.click(
                    x=self.position_x_var.get(),
                    y=self.position_y_var.get(),
                    button=self.mouse_button_var.get(),
                    clicks=clicks,
                    interval=0.001  # Reduced interval between clicks
                )
            else:
                pyautogui.click(
                    button=self.mouse_button_var.get(),
                    clicks=clicks,
                    interval=0.001  # Reduced interval between clicks
                )

            # Calculate actual delay based on CPS - NO HANDICAP
            if self.randomize_var.get():
                min_interval = self.random_min_var.get()
                max_interval = self.random_max_var.get()
                delay = random.uniform(min_interval, max_interval)
            else:
                delay = 1 / self.cps_var.get()

            # Very short delay without the handicap check
            time.sleep(max(0.001, delay))  # Just a tiny minimum to prevent system lockup

            # Decrement click count if not infinite
            if click_count > 0:
                click_count -= 1

            # REMOVED the second time.sleep that was adding extra delay

    def get_current_position(self):
        current_pos = pyautogui.position()
        self.position_x_var.set(current_pos.x)
        self.position_y_var.set(current_pos.y)

    def change_hotkey(self):
        # Create a popup window for hotkey selection
        hotkey_window = tk.Toplevel(self.root)
        hotkey_window.title("Change Hotkey")
        hotkey_window.geometry("300x150")
        hotkey_window.transient(self.root)
        hotkey_window.resizable(False, False)

        ttk.Label(hotkey_window, text="Press any key to set as hotkey:").pack(pady=15)

        hotkey_var = tk.StringVar(value=self.settings["hotkey"].upper())
        ttk.Label(hotkey_window, textvariable=hotkey_var, font=("Arial", 16)).pack(pady=10)

        def on_key_press(e):
            # Get the key from keysym
            key = e.keysym.lower()

            if key == 'escape':
                hotkey_window.destroy()
                return

            if key not in ['shift', 'control', 'alt']:
                hotkey_var.set(key.upper())
                self.settings["hotkey"] = key
                self.hotkey_label.config(text=key.upper())
                self.setup_hotkey()
                self.root.after(500, hotkey_window.destroy)

        hotkey_window.bind("<KeyPress>", on_key_press)

        # Center the window
        hotkey_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (hotkey_window.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (hotkey_window.winfo_height() // 2)
        hotkey_window.geometry(f"+{x}+{y}")

        hotkey_window.grab_set()



    def setup_hotkey(self):
        try:
            keyboard.remove_all_hotkeys()  # More thorough cleanup
        except:
            pass
        keyboard.add_hotkey(self.settings["hotkey"], self.toggle_clicking)
        print(f"Hotkey set to: {self.settings['hotkey']}")  # Add this for debugging

    def toggle_clicking(self):
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def on_close(self):
        self.stop_clicking()
        self.save_settings()
        self.root.destroy()

    def load_settings(self):
        try:
            if os.path.exists("autoclicker_settings.json"):
                with open("autoclicker_settings.json", "r") as f:
                    saved_settings = json.load(f)

                    # Handle conversion from click_interval to cps if found in saved settings
                    if "click_interval" in saved_settings:
                        saved_settings["cps"] = 1 / saved_settings["click_interval"]
                        del saved_settings["click_interval"]

                    self.settings.update(saved_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")

    def save_settings(self):
        try:
            with open("autoclicker_settings.json", "w") as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()

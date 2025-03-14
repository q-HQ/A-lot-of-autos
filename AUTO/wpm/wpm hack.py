import tkinter as tk
from tkinter import ttk
import time
import threading
import keyboard
import pyautogui
import pyperclip


class TypingSimulator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Typing Simulator")
        self.geometry("800x700")  # Fixed geometry of 800x700

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create typing simulator tab
        self.typing_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.typing_tab, text="Typing Simulator")

        # Create the input frame
        input_frame = ttk.LabelFrame(self.typing_tab, text="Input Text")
        input_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.input_text = tk.Text(input_frame, height=20, width=80, wrap=tk.WORD)
        self.input_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Control frame
        control_frame = ttk.Frame(self.typing_tab)
        control_frame.pack(fill='x', padx=10, pady=10)

        # Letters per second setting
        ttk.Label(control_frame, text="Letters Per Second:").pack(side=tk.LEFT, padx=(0, 5))
        self.lps_var = tk.StringVar(value="100")  # Default to 100 LPS
        self.lps_spinbox = ttk.Spinbox(control_frame, from_=1, to=1000, width=5,
                                       textvariable=self.lps_var)
        self.lps_spinbox.pack(side=tk.LEFT, padx=(0, 20))

        # Typing method
        ttk.Label(control_frame, text="Method:").pack(side=tk.LEFT, padx=(0, 5))
        self.typing_method = tk.StringVar(value="key_by_key")
        self.method_combo = ttk.Combobox(control_frame, textvariable=self.typing_method,
                                         values=["key_by_key", "paste_all"])
        self.method_combo.pack(side=tk.LEFT, padx=(0, 20))

        # Instructions frame
        instruction_frame = ttk.LabelFrame(self.typing_tab, text="Instructions")
        instruction_frame.pack(fill='x', padx=10, pady=10)

        instructions = (
            "1. Type your text in the box above\n"
            "2. Set typing speed in Letters Per Second (LPS)\n"
            "3. Click where you want the text to be typed (chat box, etc.)\n"
            "4. Press F12 to start typing\n"
            "5. Keep the target window focused while text is being typed"
        )
        ttk.Label(instruction_frame, text=instructions, justify=tk.LEFT).pack(padx=5, pady=5)

        # Status labels
        self.status_frame = ttk.Frame(self.typing_tab)
        self.status_frame.pack(fill='x', padx=10, pady=(5, 10))

        ttk.Label(self.status_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 5))
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.status_frame, textvariable=self.status_var).pack(side=tk.LEFT)

        ttk.Label(self.status_frame, text="Current LPS:").pack(side=tk.LEFT, padx=(20, 5))
        self.current_lps_var = tk.StringVar(value="0")
        ttk.Label(self.status_frame, textvariable=self.current_lps_var).pack(side=tk.LEFT)

        # Start button
        self.start_button = ttk.Button(self.status_frame, text="Start Typing (F12)",
                                       command=self.start_typing)
        self.start_button.pack(side=tk.RIGHT, padx=5)

        # Register F12 hotkey
        keyboard.add_hotkey('f12', self.start_typing)

        # Variable to control typing thread
        self.typing = False

    def start_typing(self):
        if self.typing:
            return  # Don't start a new thread if already typing

        text_to_type = self.input_text.get("1.0", tk.END).strip()
        if not text_to_type:
            self.status_var.set("No text to type!")
            return

        try:
            letters_per_second = float(self.lps_var.get())
            if letters_per_second <= 0:
                self.status_var.set("LPS must be positive!")
                return
        except ValueError:
            self.status_var.set("Invalid LPS value!")
            return

        # Enable typing mode
        self.typing = True
        self.start_button.config(state=tk.DISABLED)

        # Start typing in a separate thread
        threading.Thread(target=self.type_text,
                         args=(text_to_type, letters_per_second, self.typing_method.get()),
                         daemon=True).start()

    def type_text(self, text, letters_per_second, method):
        self.status_var.set("Typing...")

        # If the paste all method is selected
        if method == "paste_all":
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            self.typing = False
            self.status_var.set("Completed")
            self.start_button.config(state=tk.NORMAL)
            return

        # For key-by-key method with improved speed
        delay = 1.0 / letters_per_second  # Calculate delay between keystrokes

        # Type in chunks for better performance at high speeds
        chunk_size = 1  # Default to 1 character at a time

        # For high LPS, increase chunk size to improve performance
        if letters_per_second > 50:
            chunk_size = 5
        if letters_per_second > 200:
            chunk_size = 10
        if letters_per_second > 500:
            chunk_size = 20

        start_time = time.time()
        chars_typed = 0

        # Process text in chunks for better timing accuracy
        for i in range(0, len(text), chunk_size):
            if not self.typing:
                break

            # Get the next chunk to type
            chunk = text[i:i + chunk_size]

            # Type the chunk directly
            pyautogui.write(chunk, interval=0)

            chars_typed += len(chunk)

            # Update LPS every so often
            if i % 20 == 0:
                elapsed = time.time() - start_time
                if elapsed > 0:
                    current_lps = chars_typed / elapsed
                    self.current_lps_var.set(f"{current_lps:.1f}")

            # Sleep for the appropriate time to maintain the desired LPS
            # But account for chunk size
            time_to_sleep = (len(chunk) * delay) - 0.001  # Subtract a small offset for processing time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)

        # Final LPS calculation
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            final_lps = chars_typed / elapsed_time
            self.current_lps_var.set(f"{final_lps:.1f}")

        self.typing = False
        self.status_var.set("Completed")
        self.start_button.config(state=tk.NORMAL)

    def stop_typing(self):
        self.typing = False
        self.status_var.set("Stopped")
        self.start_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = TypingSimulator()
    app.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import time
import random


class SpeedTesterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Tester")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Main frame
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Title
        self.title_label = tk.Label(self.main_frame, text="Speed Tester", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=(0, 20))

        # Buttons frame
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack(fill="both", expand=True)

        # Create buttons
        self.clicker_button = self.create_test_button(self.buttons_frame, "CPS Clicker Test", self.start_clicker_test,
                                                      "Click as fast as possible!")
        self.wpm_button = self.create_test_button(self.buttons_frame, "WPM Typing Test", self.start_wpm_test,
                                                  "Type the sentence as fast as possible!")
        self.typer_button = self.create_test_button(self.buttons_frame, "Letter Spam Test", self.start_typer_test,
                                                    "Type a letter as many times as possible!")

        # Test frames for each test
        self.clicker_frame = self.create_test_frame()
        self.wpm_frame = self.create_test_frame()
        self.typer_frame = self.create_test_frame()

        # Variables for tests
        self.clicks = 0
        self.start_time = 0
        self.test_duration = 10  # seconds
        self.test_active = False
        self.wpm_sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "Programming is fun and rewarding when you see your code work.",
            "Python is a versatile language used for many applications.",
            "Practice makes perfect when learning to type fast.",
            "Speed tests help improve your typing and clicking abilities."
        ]
        self.target_letter = ""
        self.key_count = 0
        self.wpm_paused = False
        self.pause_time = 0

    def create_test_button(self, parent, text, command, description):
        frame = tk.Frame(parent, padx=10, pady=10)
        frame.pack(fill="x", expand=True)

        btn = tk.Button(frame, text=text, command=command,
                        font=("Arial", 12), padx=10, pady=5,
                        bg="#4CAF50", fg="white", width=15)
        btn.pack(side=tk.LEFT, padx=(0, 10))

        desc_label = tk.Label(frame, text=description, font=("Arial", 10))
        desc_label.pack(side=tk.LEFT, fill="x", expand=True)

        return btn

    def create_test_frame(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        return frame

    def show_main_menu(self):
        # Hide all test frames
        self.clicker_frame.pack_forget()
        self.wpm_frame.pack_forget()
        self.typer_frame.pack_forget()

        # Show main frame
        self.main_frame.pack(fill="both", expand=True)

    def start_clicker_test(self):
        self.main_frame.pack_forget()
        self.clicker_frame.pack_forget()
        self.clicker_frame = self.create_test_frame()
        self.clicker_frame.pack(fill="both", expand=True)

        # Reset variables
        self.clicks = 0
        self.test_active = False

        # Create UI elements
        title_label = tk.Label(self.clicker_frame, text="CPS Clicker Test", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 10))

        instruction = tk.Label(self.clicker_frame, text="Click the button as fast as possible for 10 seconds!",
                               font=("Arial", 12))
        instruction.pack(pady=(0, 20))

        self.clicks_label = tk.Label(self.clicker_frame, text="Clicks: 0", font=("Arial", 14))
        self.clicks_label.pack(pady=(0, 10))

        self.cps_label = tk.Label(self.clicker_frame, text="CPS: 0.0", font=("Arial", 14))
        self.cps_label.pack(pady=(0, 10))

        self.time_label = tk.Label(self.clicker_frame, text=f"Time remaining: {self.test_duration}s",
                                   font=("Arial", 14))
        self.time_label.pack(pady=(0, 20))

        self.click_button = tk.Button(self.clicker_frame, text="CLICK ME!", font=("Arial", 16, "bold"),
                                      bg="#FF5722", fg="white", padx=20, pady=10,
                                      command=self.register_click)
        self.click_button.pack(pady=(0, 20))

        back_button = tk.Button(self.clicker_frame, text="Back to Menu", command=self.show_main_menu)
        back_button.pack(pady=(10, 0))

    def register_click(self):
        if not self.test_active:
            self.test_active = True
            self.start_time = time.time()
            self.clicks = 0
            self.update_clicker_timer()

        self.clicks += 1
        self.clicks_label.config(text=f"Clicks: {self.clicks}")

        elapsed = time.time() - self.start_time
        if elapsed > 0:
            cps = self.clicks / elapsed
            self.cps_label.config(text=f"CPS: {cps:.2f}")

    def update_clicker_timer(self):
        elapsed = time.time() - self.start_time

        if elapsed < self.test_duration:
            time_left = self.test_duration - int(elapsed)
            self.time_label.config(text=f"Time remaining: {time_left}s")
            self.clicker_frame.after(100, self.update_clicker_timer)
        else:
            self.test_active = False
            final_cps = self.clicks / self.test_duration
            messagebox.showinfo("Test Complete", f"Your Results:\nClicks: {self.clicks}\nCPS: {final_cps:.2f}")
            self.click_button.config(state=tk.DISABLED)

    def start_wpm_test(self):
        self.main_frame.pack_forget()
        self.wpm_frame.pack_forget()
        self.wpm_frame = self.create_test_frame()
        self.wpm_frame.pack(fill="both", expand=True)

        # Reset variables
        self.test_active = False
        self.wpm_paused = False
        self.pause_time = 0

        # Create UI elements
        title_label = tk.Label(self.wpm_frame, text="WPM Typing Test", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 10))

        instruction = tk.Label(self.wpm_frame, text="Type the sentence below as fast as possible:", font=("Arial", 12))
        instruction.pack(pady=(0, 10))

        # Select random sentence
        self.target_sentence = random.choice(self.wpm_sentences)

        sentence_frame = tk.Frame(self.wpm_frame, padx=10, pady=10, bg="#E0E0E0")
        sentence_frame.pack(fill="x", pady=(0, 20))

        sentence_label = tk.Label(sentence_frame, text=self.target_sentence,
                                  font=("Arial", 12), wraplength=400, bg="#E0E0E0")
        sentence_label.pack()

        self.time_wpm_label = tk.Label(self.wpm_frame, text="Time: 0.0s", font=("Arial", 14))
        self.time_wpm_label.pack(pady=(0, 10))

        self.wpm_label = tk.Label(self.wpm_frame, text="WPM: 0.0", font=("Arial", 14))
        self.wpm_label.pack(pady=(0, 10))

        # Stats frame for displaying final results
        self.stats_frame = tk.Frame(self.wpm_frame, bg="#E8F5E9", padx=10, pady=10)
        self.final_stats_label = tk.Label(self.stats_frame, text="", font=("Arial", 12), bg="#E8F5E9", justify=tk.LEFT)
        self.final_stats_label.pack()

        typing_label = tk.Label(self.wpm_frame, text="Type here:", font=("Arial", 12))
        typing_label.pack(pady=(10, 0), anchor="w")

        self.typing_entry = tk.Entry(self.wpm_frame, font=("Arial", 12), width=50)
        self.typing_entry.pack(pady=(5, 20), fill="x")
        self.typing_entry.bind("<KeyPress>", self.on_key_wpm)
        self.typing_entry.bind("<KeyRelease>", self.check_for_period)

        # Add a try again button that will be shown after completion
        self.try_again_button = tk.Button(self.wpm_frame, text="Try Again", font=("Arial", 12),
                                          command=self.start_wpm_test)

        back_button = tk.Button(self.wpm_frame, text="Back to Menu", command=self.show_main_menu)
        back_button.pack(pady=(10, 0))

    def check_for_period(self, event):
        if self.test_active and not self.wpm_paused:
            typed_text = self.typing_entry.get()
            if typed_text.endswith("."):
                # Check if the whole sentence is typed correctly
                if typed_text == self.target_sentence:
                    self.wpm_paused = True
                    self.pause_time = time.time()
                    self.show_wpm_stats()

    def show_wpm_stats(self):
        elapsed = self.pause_time - self.start_time

        # Calculate WPM - standard formula assumes 5 chars per word
        word_count = len(self.target_sentence.split())
        char_count = len(self.target_sentence)
        wpm = (word_count / elapsed) * 60
        cpm = (char_count / elapsed) * 60  # Characters per minute

        # Display stats in the stats frame
        stats_text = (
            f"Test completed!\n\n"
            f"Time: {elapsed:.2f} seconds\n"
            f"Words: {word_count}\n"
            f"Characters: {char_count}\n"
            f"WPM: {wpm:.2f}\n"
            f"CPM: {cpm:.2f}"
        )

        self.final_stats_label.config(text=stats_text)
        self.stats_frame.pack(pady=(10, 10), fill="x")
        self.try_again_button.pack(pady=(10, 10))

        # Disable typing entry
        self.typing_entry.config(state=tk.DISABLED)

    def on_key_wpm(self, event):
        if not self.test_active and event.char and event.char.isprintable() and not self.wpm_paused:
            self.test_active = True
            self.start_time = time.time()
            self.update_wpm_timer()

    def update_wpm_timer(self):
        if self.test_active and not self.wpm_paused:
            elapsed = time.time() - self.start_time
            self.time_wpm_label.config(text=f"Time: {elapsed:.1f}s")

            # Calculate current WPM
            text = self.typing_entry.get()
            if text:
                # Simple approximation - divide by 5 chars per word
                chars = len(text)
                minutes = elapsed / 60
                if minutes > 0:
                    wpm = (chars / 5) / minutes
                    self.wpm_label.config(text=f"WPM: {wpm:.1f}")

            self.wpm_frame.after(100, self.update_wpm_timer)

    def start_typer_test(self):
        self.main_frame.pack_forget()
        self.typer_frame.pack_forget()
        self.typer_frame = self.create_test_frame()
        self.typer_frame.pack(fill="both", expand=True)

        # Reset variables
        self.test_active = False
        self.key_count = 0
        self.target_letter = random.choice("abcdefghijklmnopqrstuvwxyz").upper()

        # Create UI elements
        title_label = tk.Label(self.typer_frame, text="Letter Spam Test", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 10))

        instruction = tk.Label(
            self.typer_frame,
            text=f"Type the letter '{self.target_letter}' as many times as possible in 10 seconds!",
            font=("Arial", 12)
        )
        instruction.pack(pady=(0, 20))

        self.letter_count_label = tk.Label(self.typer_frame, text=f"Count: 0", font=("Arial", 14))
        self.letter_count_label.pack(pady=(0, 10))

        self.letter_time_label = tk.Label(self.typer_frame, text=f"Time remaining: {self.test_duration}s",
                                          font=("Arial", 14))
        self.letter_time_label.pack(pady=(0, 10))

        self.letter_entry = tk.Entry(self.typer_frame, font=("Arial", 14), width=20, justify='center')
        self.letter_entry.pack(pady=(10, 20))
        self.letter_entry.bind("<KeyPress>", self.on_key_typer)
        self.letter_entry.focus_set()

        back_button = tk.Button(self.typer_frame, text="Back to Menu", command=self.show_main_menu)
        back_button.pack(pady=(10, 0))

    def on_key_typer(self, event):
        if not self.test_active and event.char:
            self.test_active = True
            self.start_time = time.time()
            self.key_count = 0
            self.letter_entry.delete(0, tk.END)
            self.update_typer_timer()

        if self.test_active and event.char.upper() == self.target_letter:
            self.key_count += 1
            self.letter_count_label.config(text=f"Count: {self.key_count}")

    def update_typer_timer(self):
        elapsed = time.time() - self.start_time

        if elapsed < self.test_duration and self.test_active:
            time_left = self.test_duration - int(elapsed)
            self.letter_time_label.config(text=f"Time remaining: {time_left}s")
            self.typer_frame.after(100, self.update_typer_timer)
        elif self.test_active:
            self.test_active = False

            # Calculate keys per second
            kps = self.key_count / self.test_duration

            messagebox.showinfo(
                "Test Complete",
                f"Your Results:\n"
                f"Letters typed: {self.key_count}\n"
                f"Letters per second: {kps:.2f}"
            )
            self.letter_entry.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTesterApp(root)
    root.mainloop()

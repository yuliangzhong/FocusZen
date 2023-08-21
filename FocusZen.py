import tkinter as tk
from datetime import datetime, timedelta
import os

class FocusingApp:
    def __init__(self, root, schedule):
        root.title("Focus Zen \U0001F3A7")
        root.attributes("-topmost", True)
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        img = tk.PhotoImage(file=icon_path)
        root.tk.call('wm', 'iconphoto', root._w, img)

        big_font = ("Helvetica", 36)
        small_font = ("Helvetica", 18)

        self.root_ = root
        self.schedule_ = schedule

        self.label_top_ = tk.Label(root, font=big_font)
        self.label_middle_ = tk.Label(root, font=small_font)
        self.label_bottom_left_ = tk.Label(root, font=small_font)
        self.label_bottom_right_ = tk.Label(root, font=small_font)
        
        self.countdown_checkbox_var_ = tk.IntVar()
        countdown_checkbox = tk.Checkbutton(root, text="Show Countdown", font=small_font, variable=self.countdown_checkbox_var_, command=self.toggle_countdown)
        
        self.pomodoro_checkbox_var_ = tk.IntVar()
        pomodoro_checkbox = tk.Checkbutton(root, text="Pomodoro (Tomato Tick)", font=small_font, variable=self.pomodoro_checkbox_var_, command=self.toggle_tomato)
        
        # Grid layout
        self.label_top_.grid(row=0, column=0, columnspan=2, pady=10)
        self.label_middle_.grid(row=1, column=0, columnspan=2, pady=10)
        countdown_checkbox.grid(row=2, column=0, padx=(10, 0))
        pomodoro_checkbox.grid(row=2, column=1, padx=(0, 10))
        self.label_bottom_left_.grid(row=3, column=0, pady=10)
        self.label_bottom_right_.grid(row=3, column=1, pady=10)
        
        # Configure grid to expand
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        
        self.current_date_ = datetime.now().date() # assume constant (don't stay up past midnight for your own good)
        self.start_time_ = None
        self.end_time_ = None
        self.update_labels()

        self.pomodoro_end_time_ = None
                
    def update_labels(self):        
        current_time = datetime.now().time()

        if self.start_time_ is not None and self.end_time_ is not None:
            if self.start_time_ <= current_time <= self.end_time_:
                self.root_.after(100, self.update_labels)
                return
        
        for entry in self.schedule_:
            start_time, end_time = entry[0].split("-")
            start_time = datetime.strptime(start_time, "%H:%M").time()
            end_time = datetime.strptime(end_time, "%H:%M").time()
            if start_time <= current_time <= end_time:
                self.start_time_, self.end_time_ = start_time, end_time
                self.label_top_.config(text=entry[1])
                self.label_middle_.config(text=entry[2])
                if entry[2] == "":
                    self.create_text_entry_widget()
                self.root_.after(100, self.update_labels)
                return
        
        self.label_top_.config(text="No activity scheduled. Have a nice day!")
        self.label_middle_.config(text="")
        self.start_time_, self.end_time_ = None, None
        self.root_.after(100, self.update_labels)

    def toggle_tomato(self):
        if self.pomodoro_checkbox_var_.get() == 1:
            self.update_pomodoro_countdown()
    
    def toggle_countdown(self):
        if self.countdown_checkbox_var_.get() == 1:
            self.update_countdown()
        else:
            self.label_bottom_left_.config(text="")

    def update_pomodoro_countdown(self):
        if self.pomodoro_checkbox_var_.get() == 1 and self.pomodoro_end_time_ is not None:
            current_time = datetime.now().time()
            remaining_time = self.pomodoro_end_time_ - self.to_datetime(current_time)
            if remaining_time > timedelta(0):
                remaining_time_str = str(remaining_time).split(".")[0]
                self.label_bottom_right_.config(text=f"Tomato: {remaining_time_str}")
                self.root_.after(100, self.update_pomodoro_countdown)
        else:
            if self.pomodoro_end_time_ is None:
                self.pomodoro_end_time_ = datetime.now() + timedelta(minutes=25)
                self.root_.after(100, self.update_pomodoro_countdown)
            else:
                self.label_bottom_right_.config(text="")
                self.pomodoro_end_time_ = None

    def update_countdown(self):
        if self.countdown_checkbox_var_.get() == 1 and self.end_time_ is not None:
            current_time = datetime.now().time()
            remaining_time = self.to_datetime(self.end_time_) - self.to_datetime(current_time)
            if remaining_time > timedelta(0):
                remaining_time_str = str(remaining_time).split(".")[0]
                self.label_bottom_left_.config(text=f"Remaining time: {remaining_time_str}")
                self.root_.after(100, self.update_countdown)  # Update every 0.1 second
            else:
                self.label_bottom_left_.config(text="")
                self.root_.after(100, self.update_countdown)
        else:
            self.label_bottom_left_.config(text="")
    
    def to_datetime(self, t):
        return datetime.combine(self.current_date_, t)
    
    def create_text_entry_widget(self):
        if hasattr(self, "text_entry_widget"):
            return
        # Create a new text entry widget
        self.text_entry_widget = tk.Entry(self.root_, font=("Helvetica", 12))
        self.text_entry_widget.grid(row=4, column=0, columnspan=2, pady=10)

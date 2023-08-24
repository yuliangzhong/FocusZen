import tkinter as tk
from datetime import datetime, timedelta
import os
import re
import platform


# clean up and sort schedule from markdown file
def clean():
    pattern_timegap = r'\d+:\d+-\d+:\d+'
    pattern_timestamp = r'\d+:\d+'
    pattern_objective = r'\[(.*?)\]'
    pattern_tasks = r'\{(.*?)\}'
    schedule = []

    file_name = "example_schedule.md"

    with open(file_name, "r") as f:

        for line in f:
            # replace strange characters and make Chinese compatible
            sc = line.replace('*', '').replace('—','-').replace('【','[').replace('】',']').replace('：',':').strip('\n')
            objective_match = re.search(pattern_objective, sc)

            if not objective_match:
                continue

            objective = objective_match.group(1)
            task_match = re.search(pattern_tasks, sc)
            tasks = task_match.group(1) if task_match else ''

            time_gap_group = re.search(pattern_timegap, sc)
            while time_gap_group:
                time_gap = time_gap_group.group(0)
                start_time, end_time = time_gap.split("-")
                start_time = datetime.strptime(start_time, "%H:%M").time()
                end_time = datetime.strptime(end_time, "%H:%M").time()
                if start_time > end_time:
                    continue
                schedule.append([start_time, end_time, objective, tasks])
                sc = sc.replace(time_gap, '')
                time_gap_group = re.search(pattern_timegap, sc)

            timestamp_match = re.search(pattern_timestamp, sc)
            if timestamp_match:
                timestamp = timestamp_match.group(0)
                start_time = datetime.strptime(timestamp, "%H:%M").time()
                end_time = (datetime.strptime(timestamp, "%H:%M") + timedelta(minutes=1)).time()
                schedule.append([start_time, end_time, objective, tasks])
    
    # sort schedule by start time. If start time is the same, sort by end time
    schedule.sort(key=lambda x: (x[0], x[1]))

    return schedule


class FocusingApp:
    def __init__(self, root, schedule):
        # Set up window
        root.title("Focus Zen \U0001F3A7")
        root.attributes("-topmost", True)
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        img = tk.PhotoImage(file=icon_path)
        root.tk.call('wm', 'iconphoto', root._w, img)
        system = platform.system() == 'Linux'

        # Set up fonts
        big_font = ("Ubuntu Regular", 24) if system else ("Helvetica", 24)
        small_font = ("Ubuntu Regular", 15) if system else ("Helvetica", 15)

        self.root_ = root
        self.schedule_ = schedule

        self.label_top_ = tk.Label(root, text="", font=big_font)
        self.label_middle_ = tk.Label(root, text="", font=small_font)
        self.label_bottom_left_ = tk.Label(root, text="", font=small_font)
        self.label_bottom_right_ = tk.Label(root, text="", font=small_font)
        root.bind('<Configure>', lambda _: self.label_middle_.config(wraplength=self.root_.winfo_width() - 20))

        self.text_widget_ = tk.Text(root, width=self.root_.winfo_width(), height=1, font=small_font)
        self.text_widget_.bind('<KeyPress-Return>', lambda _: self.text_widget_.config(height=self.text_widget_.index('end').split('.')[0]))
        self.text_widget_.bind('<BackSpace>', lambda _: self.text_widget_.config(height=self.text_widget_.index('end-2c').split('.')[0]))
        self.text_widget_.bind('<Button-1>', lambda _: self.text_widget_.config(insertbackground='black'))
        self.text_widget_.bind('<FocusOut>', lambda _: self.text_widget_.config(insertbackground='white'))
        self.save_button_ = tk.Button(root, text="\U0001F4BE", width=1, height=1 if system else 2, font=small_font, command=self.save_to_file)
        # if emoji won't show up, $ sudo apt install unifont

        self.countdown_checkbox_var_ = tk.IntVar()
        countdown_checkbox = tk.Checkbutton(root, text="Show Countdown", font=small_font, variable=self.countdown_checkbox_var_)
        self.pomodoro_checkbox_var_ = tk.IntVar()
        pomodoro_checkbox = tk.Checkbutton(root, text="Pomodoro (Tomato Tick)", font=small_font, variable=self.pomodoro_checkbox_var_)
        
        # Grid layout
        self.label_top_.grid(row=0, column=0, columnspan=2, pady=5)
        self.label_middle_.grid(row=1, column=0, columnspan=2, pady=5)
        countdown_checkbox.grid(row=2, column=0, padx=(5, 0))
        pomodoro_checkbox.grid(row=2, column=1, padx=(0, 5))
        self.label_bottom_left_.grid(row=3, column=0, pady=5)
        self.label_bottom_right_.grid(row=3, column=1, pady=5)
        self.text_widget_.grid(row=4, column=0, columnspan=2, padx=(10, 60), pady=5, sticky="ew")
        self.save_button_.grid(row=4, column=1, padx=(0, 10), pady=5, sticky="e")
        
        # Grid configuration
        for i in range(5):
            root.grid_rowconfigure(i, weight=1)
        for i in range(2):
            root.grid_columnconfigure(i, weight=1)
        
        # Find current activity
        self.id_, self.time_before_, self.time_after_ = None, None, None
        current_time = datetime.now().time()
        for i in range(len(self.schedule_) - 1, -1, -1):
            if current_time <= self.schedule_[i][0]:
                continue
            else:
                if current_time <= self.schedule_[i][1]:
                    self.id_, self.time_before_, self.time_after_ = i, self.schedule_[i][0], self.schedule_[i][1]
                    self.label_top_.config(text=self.schedule_[i][2])
                    self.label_middle_.config(text=self.schedule_[i][3])
                else:
                    if i == len(self.schedule_) - 1:
                        self.label_top_.config(text="No more activities today! Good night \U0001F634")
                        return
                    else:
                        self.id_, self.time_before_, self.time_after_ = i, self.schedule_[i][1], self.schedule_[i + 1][0]
                        self.label_top_.config(text="Coffee time now! \U00002615")
                break

        if self.id_ is None:
            self.label_top_.config(text="Early bird catches the worm! Have a nice day! \U0001F423")
            self.time_after_ = self.schedule_[0][0]
        
        # set text widget width as the width of top label
        self.text_widget_.config(width=len(self.label_top_.cget("text")))

        # other configs
        self.current_date_ = datetime.now().date() # assume constant (don't stay up past midnight for your own good)
        self.pomodoro_end_time_ = None
        self.loop()


    def loop(self):
        current_time = datetime.now().time()

        exit_flag = self.update_labels(current_time)
        self.update_countdown(current_time)
        self.update_pomodoro_countdown(current_time)

        if not exit_flag:
            self.root_.after(100, self.loop)


    def update_labels(self, current_time):
        if current_time <= self.time_after_:
            return
        else:
            if self.id_ == len(self.schedule_) - 1:
                self.label_top_.config(text="No more activities today! Good night \U0001F634")
                self.label_middle_.config(text="")
                return True
            else:
                if self.time_after_ == self.schedule_[self.id_ + 1][0]:
                    self.id_, self.time_before_, self.time_after_ = self.id_ + 1, self.schedule_[self.id_ + 1][0], self.schedule_[self.id_ + 1][1]
                    self.label_top_.config(text=self.schedule_[self.id_][2])
                    self.label_middle_.config(text=self.schedule_[self.id_][3])
                else:
                    self.id_, self.time_before_, self.time_after_ = self.id_, self.schedule_[self.id_][1], self.schedule_[self.id_ + 1][0]
                    self.label_top_.config(text="Coffee time now! \U00002615")
                    self.label_middle_.config(text="")
            return False
    

    def update_countdown(self, current_time):
        if self.countdown_checkbox_var_.get() == 1:
            remaining_time = self.to_datetime(self.time_after_) - self.to_datetime(current_time)
            if remaining_time > timedelta(0):
                # print current time
                self.label_bottom_left_.config(text=f"{str(remaining_time).split('.')[0]}")
        else:
            self.label_bottom_left_.config(text="")
    

    def update_pomodoro_countdown(self, current_time):
        if self.pomodoro_checkbox_var_.get() == 1:
            if self.pomodoro_end_time_ is None:
                self.pomodoro_end_time_ = (self.to_datetime(current_time) + timedelta(minutes=25)).replace(microsecond=0)
            
            remaining_time = self.pomodoro_end_time_ - self.to_datetime(current_time)
            if remaining_time > timedelta(0):
                self.label_bottom_right_.config(text=f"{str(remaining_time).split('.')[0]}")
        else:
            self.pomodoro_end_time_ = None
            self.label_bottom_right_.config(text="")


    def to_datetime(self, t):
        return datetime.combine(self.current_date_, t)


    def save_to_file(self):
        content = self.text_widget_.get("1.0", "end-1c")
        current_date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open("notebook.txt", "a") as file:
            file.write("[" + current_date_and_time + "]\n" + content + "\n")
        self.text_widget_.delete("1.0", "end-1c")
        self.text_widget_.config(height=1)

def main():
    schedule = clean()
    root = tk.Tk()
    FocusingApp(root, schedule)
    root.mainloop()


if __name__ == "__main__":
    main()
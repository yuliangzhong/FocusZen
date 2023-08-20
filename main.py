import re
import tkinter as tk
from datetime import datetime
from FocusingApp import FocusingApp

def clean():
    pattern_timegap = r'\d+:\d+-\d+:\d+'
    pattern_objective = r'\[(.*?)\]'
    pattern_tasks = r'\{(.*?)\}'
    schedule = []

    file_name = "schedule_weekends.txt" if datetime.now().weekday() in [6,7] else "schedule_weekdays.txt"

    with open(file_name, "r") as f:
        objective = None
        tasks = None

        for line in f:
            # replace strange characters
            sc = line.replace('*', '').replace('—','-').replace('【','[').replace('】',']').strip('\n')
            objective_match = re.search(pattern_objective, sc)

            if not objective_match:
                continue

            objective = objective_match.group(1)
            task_match = re.search(pattern_tasks, sc)
            tasks = task_match.group(1) if task_match else ''

            time_gap_group = re.search(pattern_timegap, sc)
            while time_gap_group:
                time_gap = time_gap_group.group(0)
                schedule.append([time_gap, objective, tasks])
                sc = sc.replace(time_gap, '')
                time_gap_group = re.search(pattern_timegap, sc)

    return schedule

def main():
    schedule = clean()
    root = tk.Tk()
    FocusingApp(root, schedule)
    root.mainloop()


if __name__ == "__main__":
    main()

# To run in background:
# python main.py & ps aux | grep "python main.py"
# kill -9 <pid>
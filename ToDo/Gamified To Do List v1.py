import tkinter as tk
from tkinter import ttk
import json

# {
#     "description": "Read a chapter of textbook",
#     "tag": "study",
#     "points": 10,
#     "completed": False
# }

TAG_POINTS = {
    "study": 10,
    "exercise": 15,
    "chores": 5,
    "work": 12,
    "creative": 8,
    "coding": 7
}

tasks = []
LEVEL_THRESHOLDS = [0, 50, 150, 300, 500, 800]


class TaskApp:
    def __init__(self, window):
        self.window = window
        self.window.title("ToDo")
        self.window.geometry("600x500")  # Optional: make it a bit wider

        self.task_var = tk.StringVar()
        self.tag_var = tk.StringVar(value="study")
        self.total_points = 0
        self.level = 1

        # ===== ROW 0: Task input row =====
        tk.Label(window, text="Task:").grid(row=0, column=0, padx=5, pady=10, sticky="e")
        tk.Entry(window, textvariable=self.task_var, width=30).grid(row=0, column=1, padx=5, pady=10, columnspan=2)

        tk.Label(window, text="Tag:").grid(row=0, column=3, padx=5, sticky="e")
        self.tag_menu = ttk.Combobox(window, textvariable=self.tag_var, values=list(TAG_POINTS.keys()), width=10)
        self.tag_menu.grid(row=0, column=4, padx=5)

        tk.Button(window, text="Add Task", command=self.add_task).grid(row=0, column=5, padx=10)

        # ===== ROW 1: Task checklist frame =====
        self.task_frame = tk.Frame(window)
        self.task_frame.grid(row=1, column=0, columnspan=6, pady=20, sticky="nsew")

        # ===== ROW 2: Points and level =====
        self.points_label = tk.Label(window, text="Today's Total Points: 0", font=("Helvetica", 12, "bold"))
        self.points_label.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        # self.level_label = tk.Label(window, text="Level: 1", font=("Helvetica", 12, "bold"))
        # self.level_label.grid(row=2, column=2, columnspan=2, pady=10, padx=5)

        self.progress = ttk.Progressbar(window, length=150, maximum=100)
        self.progress.grid(row=2, column=4, columnspan=2, pady=10, padx=10)

        self.level_label = tk.Label(window, text="Level: 1")
        self.level_label.grid(row=2, column=2)
        self.level_up_label = tk.Label(self.window, text="🎉 Level Up! 🎉", font=("Helvetica", 16, "bold"), fg="gray")
        self.level_up_label.lower()  # Hide it behind everything initially

        # ===== ROW 3: Save/Load buttons =====
        btn_frame = tk.Frame(window)
        btn_frame.grid(row=3, column=0, columnspan=6, pady=10)

        tk.Button(btn_frame, text="💾 Save Tasks", command=self.save_tasks).pack(side="left", padx=10)
        tk.Button(btn_frame, text="📂 Load Tasks", command=self.load_tasks).pack(side="left", padx=10)

    def add_task(self):
        task_desc = self.task_var.get()
        tag = self.tag_var.get()
        if task_desc:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.task_frame, text=f"{task_desc} [{tag}]", variable=var,
                                command=lambda: self.toggle_task(var, tag))
            cb.pack(anchor='w')
            tasks.append({"text": task_desc, "tag": tag, "var": var, "checkbox": cb})

    def toggle_task(self, var, tag):
        points = TAG_POINTS.get(tag, 0)
        if var.get():
            self.total_points += points
        else:
            self.total_points -= points

        self.points_label.config(text=f"Today's Total Points: {self.total_points}")
        self.update_level()

    def update_level(self):
        previous_level = self.level
        for i in range(len(LEVEL_THRESHOLDS)):
            if self.total_points < LEVEL_THRESHOLDS[i]:
                self.level = i
                break
            else:
                self.level = len(LEVEL_THRESHOLDS)

        if self.level > previous_level:
            self.animate_level_up()
            self.show_confetti_popup()  # 🎉🎊 the real party
            for i in range(len(LEVEL_THRESHOLDS)):
                if self.total_points < LEVEL_THRESHOLDS[i]:
                    self.level = i
                    break
                else:
                    self.level = len(LEVEL_THRESHOLDS)

        # Get XP progress toward next level
        current_level_min = LEVEL_THRESHOLDS[self.level - 1] if self.level > 1 else 0
        current_level_max = LEVEL_THRESHOLDS[self.level] if self.level < len(LEVEL_THRESHOLDS) else self.total_points + 100
        progress_within_level = self.total_points - current_level_min
        progress_range = current_level_max - current_level_min
        progress_percent = (progress_within_level / progress_range) * 100

        # Update progress bar + label
        self.progress["value"] = progress_percent
        self.level_label.config(text=f"Level: {self.level}")

    def animate_level_up(self):
        self.level_up_label.lift()  # Bring label to front
        self.level_up_label.after(0, lambda: self.level_up_label.config(fg="green"))
        self.level_up_label.after(1000, lambda: self.level_up_label.lower())

    def show_confetti_popup(self):
        popup = tk.Toplevel(self.window)
        popup.title("🎉 Level Up! 🎉")
        popup.geometry("300x150+500+300")  # Size and position

        popup_label = tk.Label(
            popup,
            text="🎊🎉🎈💫🎆✨🎉🎊\nYou leveled up!\n🎊🎉🎈💫🎆✨🎉🎊",
            font=("Helvetica", 14),
            fg="purple"
        )
        popup_label.pack(expand=True)

        # Close the popup after 1.5 seconds
        popup.after(1500, popup.destroy)

    def save_tasks(self):
        data = []
        for task in tasks:
            data.append({
                "text": task["text"],
                "tag": task["tag"],
                "completed": task["var"].get()
            })
        with open("tasks.json", "w") as file:
            json.dump(data, file)
        print("Tasks saved!")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                data = json.load(file)
                self.total_points = 0
                self.points_label.config(text=f"Total Points: {self.total_points}")
                for widget in self.task_frame.winfo_children():
                    widget.destroy()
                tasks.clear()
                for item in data:
                    var = tk.BooleanVar(value=item["completed"])
                    cb = tk.Checkbutton(self.task_frame, text=f"{item['text']} [{item['tag']}]", variable=var,
                                        command=lambda v=var, t=item["tag"]: self.toggle_task(v, t))
                    cb.pack(anchor='w')
                    tasks.append({"text": item["text"], "tag": item["tag"], "var": var, "checkbox": cb})
                    if item["completed"]:
                        self.toggle_task(var, item["tag"])
            print("Tasks loaded!")
        except FileNotFoundError:
            print("No saved file found yet.")


window = tk.Tk() #main window
app = TaskApp(window)
window.mainloop()  #Keeps the window open and listening for user events


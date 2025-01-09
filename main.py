import calendar
import customtkinter as ctk
from datetime import datetime
import json

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x400")
        self.root.title("Interactive Calendar")

        # Get current month and year
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month


        self.activities_file = "activities.json"
        self.activities = self.load_activities()

        self.header = ctk.CTkLabel(
            self.root, 
            text=f"{calendar.month_name[self.current_month]} {self.current_year}", 
            font=("Arial", 20),
            fg_color="skyblue",
            corner_radius=10
        )
        self.header.pack(pady=10)

        self.calendar_frame = ctk.CTkFrame(self.root)
        self.calendar_frame.pack(expand=True, fill="both", pady=10)

        self.navigation_frame = ctk.CTkFrame(self.root)
        self.navigation_frame.pack()

        self.prev_button = ctk.CTkButton(
            self.navigation_frame, 
            text="<", 
            command=self.prev_month
        )
        self.prev_button.pack(side="left", padx=10)

        self.next_button = ctk.CTkButton(
            self.navigation_frame, 
            text=">", 
            command=self.next_month
        )
        self.next_button.pack(side="left", padx=10)

        self.view_button = ctk.CTkButton(
            self.root, 
            text="View Activities", 
            command=self.view_activities
        )
        self.view_button.pack(pady=10)

        # Generate the calendar
        self.generate_calendar()

    # Get contents from the json file
    def load_activities(self):
        try:
            with open(self.activities_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    # Save activities to the json file
    def save_activities(self):
        with open(self.activities_file, "w") as f:
            json.dump(self.activities, f, indent=4)

    def generate_calendar(self):
        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Days of the week
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for day in days:
            label = ctk.CTkLabel(self.calendar_frame, text=day, font=("Arial", 12))
            label.grid(row=0, column=days.index(day), padx=5, pady=5)

        cal = calendar.Calendar()
        month_days = cal.itermonthdays(self.current_year, self.current_month)
        row = 1
        col = 0

        for day in month_days:
            if day == 0:
                col += 1
                continue

            btn = ctk.CTkButton(
                self.calendar_frame,
                text=str(day),
                command=lambda d=day: self.on_date_click(d),
                width=40
            )
            btn.grid(row=row, column=col, padx=5, pady=5)

            col += 1
            if col > 6:
                col = 0
                row += 1

    def on_date_click(self, day):
        self.open_activity_window(day)

    def open_activity_window(self, day):
        activity_window = ctk.CTkToplevel(self.root)
        activity_window.geometry("300x200")
        activity_window.title(f"""Set Activity for {day} {calendar.month_name[self.current_month]} 
                                {self.current_year}""")

        label = ctk.CTkLabel(activity_window, text="Enter Activity:", font=("Arial", 14))
        label.pack(pady=10)

        activity_entry = ctk.CTkEntry(activity_window, width=200)
        activity_entry.pack(pady=10)

        set_button = ctk.CTkButton(
            activity_window,
            text="Set Activity",
            command=lambda: self.set_activity(day, activity_entry.get(), activity_window)
        )
        set_button.pack(pady=10)

    def set_activity(self, day, activity, window):
        date_key = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
        self.activities[date_key] = activity
        self.save_activities()
        window.destroy()

    def view_activities(self):
        view_window = ctk.CTkToplevel(self.root)
        view_window.geometry("400x300")
        view_window.title("All Activities")

        if not self.activities:
            label = ctk.CTkLabel(view_window, text="No activities set.", font=("Arial", 14))
            label.pack(pady=10)
        else:
            for date, activity in self.activities.items():
                frame = ctk.CTkFrame(view_window)
                frame.pack(fill="x", padx=10, pady=5)

                activity_label = ctk.CTkLabel(
                    frame, 
                    text=f"{date}: {activity}", 
                    font=("Arial", 12)
                )
                activity_label.pack(side="left", padx=10)

                edit_button = ctk.CTkButton(
                    frame, 
                    text="Edit", 
                    width= 50,
                    height=20,
                    command=lambda d=date, a=activity: self.edit_activity(d, a, view_window)
                )
                edit_button.pack(side="right", padx=10)

                delete_button = ctk.CTkButton(
                    frame, 
                    text="Delete",
                    fg_color="red",
                    width= 50,
                    height=20,
                    command=lambda d=date: self.delete_activity(d, view_window)
                )
                delete_button.pack(side="right", padx=10)

    def delete_activity(self, date, parent_window):
        if date in self.activities:
            del self.activities[date]
            self.save_activities()
            parent_window.destroy()
            self.view_activities()  # Refresh the activities list


    def edit_activity(self, date, current_activity, parent_window):
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.geometry("300x200")
        edit_window.title(f"Edit Activity for {date}")

        label = ctk.CTkLabel(edit_window, text="Update Activity:", font=("Arial", 14))
        label.pack(pady=10)

        activity_entry = ctk.CTkEntry(edit_window, width=200)
        activity_entry.insert(0, current_activity)
        activity_entry.pack(pady=10)

        update_button = ctk.CTkButton(
            edit_window,
            text="Update",
            command=lambda: self.update_activity(date, activity_entry.get(), edit_window, parent_window)
        )
        update_button.pack(pady=10)

    def update_activity(self, date, new_activity, edit_window, parent_window):
        self.activities[date] = new_activity
        self.save_activities()
        edit_window.destroy()
        parent_window.destroy()
        self.view_activities()  



    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()

    def update_calendar(self):
        self.header.configure(text=f"{calendar.month_name[self.current_month]} {self.current_year}")
        self.generate_calendar()

if __name__ == "__main__":
    app = ctk.CTk()
    CalendarApp(app)
    app.mainloop()

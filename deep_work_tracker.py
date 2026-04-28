import tkinter as tk
import time
import csv
import os
from datetime import datetime

# Automatically find the directory where this script is saved
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Force the CSV to be saved in that exact directory
LOG_FILE = os.path.join(SCRIPT_DIR, "deep_work_log.csv")


class DeepWorkTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Deep Work Tracker")
        self.root.geometry("300x180")  # Made slightly taller to fit the new buttons
        self.root.attributes("-topmost", True)

        # Initialize the CSV if it doesn't exist
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Elapsed_Minutes"])

        # Time tracking variables
        self.start_time = None
        self.is_working = False
        self.is_paused = False
        self.pause_start_time = None
        self.total_paused_time = 0.0

        # Initial UI Setup
        self.label = tk.Label(
            root, text="Are you doing work or leisure?", font=("Arial", 12)
        )
        self.label.pack(pady=15)

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack()

        self.work_btn = tk.Button(
            self.btn_frame,
            text="Work",
            command=self.start_work,
            width=10,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        self.work_btn.pack(side=tk.LEFT, padx=10)

        self.leisure_btn = tk.Button(
            self.btn_frame,
            text="Leisure",
            command=self.exit_app,
            width=10,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        self.leisure_btn.pack(side=tk.RIGHT, padx=10)

        # Ensure closing the window logs the time properly
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_work(self):
        self.start_time = time.time()
        self.is_working = True

        # Update UI to the active session state
        self.label.config(text="Deep work session active.\nClose window to stop & log.")
        self.btn_frame.pack_forget()

        # New frame for active session buttons
        self.active_btn_frame = tk.Frame(self.root)
        self.active_btn_frame.pack(pady=10)

        self.pause_btn = tk.Button(
            self.active_btn_frame,
            text="Pause",
            command=self.toggle_pause,
            width=10,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        self.pause_btn.pack(side=tk.LEFT, padx=10)

        self.stop_btn = tk.Button(
            self.active_btn_frame,
            text="Stop & Log",
            command=self.log_and_exit,
            width=10,
            bg="#F44336",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        self.stop_btn.pack(side=tk.RIGHT, padx=10)

        # ADD THIS LINE: Minimizes the window to the taskbar
        self.root.iconify()

    def toggle_pause(self):
        if not self.is_paused:
            # Action: Pause the timer
            self.is_paused = True
            self.pause_start_time = time.time()
            self.pause_btn.config(
                text="Resume", bg="#2196F3"
            )  # Change to a blue resume button
            self.label.config(text="Session paused.\nGo take a break.")
        else:
            # Action: Resume the timer
            self.is_paused = False
            self.total_paused_time += time.time() - self.pause_start_time
            self.pause_btn.config(
                text="Pause", bg="#FF9800"
            )  # Revert to orange pause button
            self.label.config(
                text="Deep work session active.\nClose window to stop & log."
            )

    def log_time(self):
        if self.is_working and self.start_time:
            # If the app is closed while currently paused, finalize the pause math
            if self.is_paused:
                self.total_paused_time += time.time() - self.pause_start_time

            # Calculate pure work time
            elapsed_seconds = time.time() - self.start_time - self.total_paused_time

            # Failsafe: only log if time is positive (prevents weird bugs logging 0 or negative time)
            if elapsed_seconds > 0:
                elapsed_minutes = round(elapsed_seconds / 60, 2)
                today = datetime.now().strftime("%Y-%m-%d")

                # Read existing data
                log_data = {}
                if os.path.exists(LOG_FILE):
                    with open(LOG_FILE, "r") as f:
                        reader = csv.reader(f)
                        next(reader, None)  # Skip header
                        for row in reader:
                            if row:
                                log_data[row[0]] = float(row[1])

                # Add current session to today's cumulative total
                log_data[today] = log_data.get(today, 0.0) + elapsed_minutes

                # Write back to CSV
                with open(LOG_FILE, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Date", "Elapsed_Minutes"])
                    for date_key, mins in log_data.items():
                        writer.writerow([date_key, round(mins, 2)])

    def log_and_exit(self):
        self.log_time()
        self.root.destroy()

    def on_closing(self):
        self.log_time()
        self.root.destroy()

    def exit_app(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DeepWorkTracker(root)
    root.mainloop()

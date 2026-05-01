import tkinter as tk
import time
import csv
import os
from datetime import datetime, timedelta

# Automatically find the directory where this script is saved
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Force the CSVs to be saved in that exact directory
LOG_FILE = os.path.join(SCRIPT_DIR, "deep_work_log.csv")
HOURLY_LOG_FILE = os.path.join(SCRIPT_DIR, "deep_work_hourly.csv")


class DeepWorkTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Deep Work Tracker")
        self.root.geometry("300x180")
        self.root.attributes("-topmost", True)

        # Initialize the Daily CSV if it doesn't exist
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Elapsed_Minutes"])

        # Initialize the Hourly CSV if it doesn't exist
        if not os.path.exists(HOURLY_LOG_FILE):
            with open(HOURLY_LOG_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Hour", "Elapsed_Minutes"])

        # Time tracking variables
        self.is_working = False
        self.is_paused = False
        self.current_session_start = None
        self.work_intervals = (
            []
        )  # Stores chunks of work as (start_timestamp, end_timestamp)

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

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_work(self):
        self.is_working = True
        self.current_session_start = time.time()

        self.label.config(text="Deep work session active.\nClose window to stop & log.")
        self.btn_frame.pack_forget()

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

        self.root.iconify()

    def toggle_pause(self):
        if not self.is_paused:
            if self.current_session_start:
                self.work_intervals.append((self.current_session_start, time.time()))

            self.is_paused = True
            self.current_session_start = None
            self.pause_btn.config(text="Resume", bg="#2196F3")
            self.label.config(text="Session paused.\nGo take a break.")
        else:
            self.current_session_start = time.time()
            self.is_paused = False
            self.pause_btn.config(text="Pause", bg="#FF9800")
            self.label.config(
                text="Deep work session active.\nClose window to stop & log."
            )

    def log_time(self):
        if self.is_working:
            if not self.is_paused and self.current_session_start:
                self.work_intervals.append((self.current_session_start, time.time()))

            if not self.work_intervals:
                return

            # --- PROCESS DAILY LOG ---
            daily_log_data = {}
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    for row in reader:
                        if row:
                            # Safety check: Handle both the old 2-column and new 3-column formats seamlessly
                            if len(row) == 2:
                                daily_log_data[row[0]] = float(row[1])
                            elif len(row) == 3:
                                daily_log_data[row[0]] = float(row[2])

            # --- PROCESS HOURLY LOG ---
            hourly_log_data = {}
            if os.path.exists(HOURLY_LOG_FILE):
                with open(HOURLY_LOG_FILE, "r") as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    for row in reader:
                        if len(row) == 3:
                            d, h, m = row[0], row[1], float(row[2])
                            if d not in hourly_log_data:
                                hourly_log_data[d] = {}
                            hourly_log_data[d][h] = m

            # Slice and dice the intervals for both files
            for start_ts, end_ts in self.work_intervals:
                self._process_daily_interval(start_ts, end_ts, daily_log_data)
                self._process_hourly_interval(start_ts, end_ts, hourly_log_data)

            # --- WRITE BACK DAILY LOG (Now with Day of the Week) ---
            with open(LOG_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Day_of_Week", "Elapsed_Minutes"])
                for date_key in sorted(daily_log_data.keys()):
                    # Automatically figure out the day of the week from the date
                    day_name = datetime.strptime(date_key, "%Y-%m-%d").strftime("%A")
                    writer.writerow(
                        [date_key, day_name, round(daily_log_data[date_key], 2)]
                    )

            # --- WRITE BACK HOURLY LOG ---
            with open(HOURLY_LOG_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Hour", "Elapsed_Minutes"])
                for d in sorted(hourly_log_data.keys()):
                    for h in sorted(hourly_log_data[d].keys()):
                        writer.writerow([d, h, round(hourly_log_data[d][h], 2)])

    def _process_daily_interval(self, start_ts, end_ts, log_data):
        """Slices a time interval into days if it crosses midnight."""
        current_start = start_ts
        while current_start < end_ts:
            dt_start = datetime.fromtimestamp(current_start)
            next_midnight = datetime(
                dt_start.year, dt_start.month, dt_start.day
            ) + timedelta(days=1)

            chunk_end_ts = min(end_ts, next_midnight.timestamp())
            elapsed_minutes = (chunk_end_ts - current_start) / 60.0

            if elapsed_minutes > 0:
                date_str = dt_start.strftime("%Y-%m-%d")
                log_data[date_str] = log_data.get(date_str, 0.0) + elapsed_minutes

            current_start = chunk_end_ts

    def _process_hourly_interval(self, start_ts, end_ts, hourly_log_data):
        """Slices a time interval precisely by the hour."""
        current_start = start_ts
        while current_start < end_ts:
            dt_start = datetime.fromtimestamp(current_start)

            # Find the exact timestamp of the top of the next hour
            next_hour = (dt_start + timedelta(hours=1)).replace(
                minute=0, second=0, microsecond=0
            )

            chunk_end_ts = min(end_ts, next_hour.timestamp())
            elapsed_minutes = (chunk_end_ts - current_start) / 60.0

            if elapsed_minutes > 0:
                date_str = dt_start.strftime("%Y-%m-%d")
                hour_str = dt_start.strftime(
                    "%H:00"
                )  # Formats as "09:00", "14:00", etc.

                if date_str not in hourly_log_data:
                    hourly_log_data[date_str] = {}

                hourly_log_data[date_str][hour_str] = (
                    hourly_log_data[date_str].get(hour_str, 0.0) + elapsed_minutes
                )

            current_start = chunk_end_ts

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

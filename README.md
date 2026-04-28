This script is a program to track how much work you're doing.

# Deep Work Tracker ⏱️

A frictionless, lightweight Python desktop app to track your work time.

Built for people who want to track their productivity but hate the friction of web apps, manual timers, and subscription fees. It runs locally, pops up exactly when you need it, and saves your data to a simple `.csv` file that you own.

## Features

- **Zero Friction:** A simple UI that asks "Work or Leisure?".
- **Background Timer:** Keeps track of your deep work minutes in the background.
- **Pause/Resume:** Accurately calculates your time even if you need to step away for a break.
- **Failsafe Logging:** Automatically calculates and logs your time even if you force-close the window or shut down your PC.
- **Local Data:** Saves everything to a `deep_work_log.csv` file that you can easily plug into Excel, Pandas, or Notion. No cloud tracking.

## Prerequisites

- Python 3.x installed on your machine.
- No external libraries required! It uses Python's built-in `tkinter`, `csv`, and `datetime` modules.

## Setup & Installation

1. Clone this repository:

   git clone [https://github.com/lricketson/deep-work-tracker.git](https://github.com/lricketson/deep-work-tracker.git)
   cd deep-work-tracker

2. Run the script:
   python deep_work_tracker.py
   (Note: Use pythonw instead of python on Windows to run the script silently without opening a terminal window).

   ### Recommended Workflow (Frictionless Setup)

   To get the most out of this tracker, you shouldn't have to launch it manually. Here is how to set it up so it is always one click away.

   #### For Windows Users:

   #### Method 1: Desktop Shortcut (Manual Trigger)
   1. Right-click your desktop -> New -> Shortcut.
   2. Paste the following (update the path to match your machine):
      pythonw "C:\path\to\your\folder\deep_work_tracker.py
   3. "Name it "Work Tracker" and pin it to your taskbar. Click it whenever you sit down to work.

   #### Method 2: Launch on Startup (Automatic Trigger)

   To have the tracker ask you "Work or Leisure?" the second you log into your computer:
   1. Open Windows Task Scheduler.
   2. Create a New Task (Run with highest privileges).
   3. Trigger: At log on.
   4. Action: Start a program.
   - Program: pythonw
   - Arguments: "C:\path\to\your\folder\deep_work_tracker.py"
   - Start in: C:\path\to\your\folder\

   #### For macOS/Linux Users:

   You can set the tracker to launch automatically on boot using cron.
   1. Open your terminal and type crontab -e.
   2. Add the following line (update with your actual paths):
      @reboot /usr/bin/python3 /path/to/your/deep_work_tracker.py &

   ### Data Storage

   Your data is automatically saved in deep_work_log.csv in the same directory as the script. It aggregates your work cumulatively by day, looking like this:
   Date Elapsed_Minutes
   2026-04-28 145.50
   2026-04-29 210.25

   ### License

   MIT License - feel free to modify, fork, and use!

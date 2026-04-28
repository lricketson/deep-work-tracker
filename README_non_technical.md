## 🧭 Super Simple Setup (For Non-Tech People)

If you aren't super familiar with computers, don't worry. You can still use this. Just follow these exact steps:

### Step 1: Install Python (The Engine)

This app runs on a language called Python. If you don't have it, you need to download it first.

1. Go to [python.org/downloads](https://www.python.org/downloads/) and click the big yellow **Download Python** button.
2. Open the file you just downloaded to install it.
3. **🚨 CRUCIAL STEP FOR WINDOWS USERS:** At the very bottom of the first installation screen, there is a small checkbox that says **"Add Python to PATH"**. You **MUST** check this box before clicking "Install Now".
4. Finish the installation.

### Step 2: Download This Tracker (The App)

1. Scroll to the top of this GitHub page.
2. Click the green **"<> Code"** button.
3. Click **"Download ZIP"**.
4. Find the downloaded ZIP file on your computer (usually in your Downloads folder), right-click it, and select **"Extract All..."**.
5. Move that extracted folder somewhere safe where you won't accidentally delete it, like your `Documents` folder.

### Step 3: Make it Automatic (Pop up when you open your laptop)

To get the ultimate frictionless experience, we will tell your computer to launch this app the exact second you log in.

**For Windows:**
We will use a built-in tool called Task Scheduler.

1. Click your Windows Start button, type **Task Scheduler**, and hit Enter.
2. On the right-hand menu, click **Create Task...** (Make sure you click this one, _not_ "Create Basic Task").
3. A window with several tabs will pop up.
   - **General Tab:** Name it "Deep Work Tracker". At the bottom, check the box that says **Run with highest privileges**.
   - **Triggers Tab:** Click **New...** at the bottom. Change the top dropdown to **At log on**, then click OK.
   - **Actions Tab:** Click **New...** \* In the **Program/script** box, type exactly: `pythonw`
     - In the **Add arguments** box, paste the exact path to your file, surrounded by quotes. _(Example: `"C:\Users\YourName\Documents\deep-work-tracker\deep_work_tracker.py"`)_
     - In the **Start in** box, paste the path to your folder, _without_ quotes. _(Example: `C:\Users\YourName\Documents\deep-work-tracker\`)_
     - Click OK.
   - **Conditions Tab:** _Crucial step if you use a laptop!_ Uncheck the box that says **Start the task only if the computer is on AC power**. (If you leave this checked, it won't pop up when you are on battery power).
4. Click **OK** at the very bottom to save your task.

**For Mac:**
We are going to use a built-in Mac tool called Automator.

1. Open the **Automator** app (Press `Cmd + Space` and type "Automator").
2. Click **New Document**, select **Application** from the icons, and click **Choose**.
3. In the search bar at the top left, type **Run Shell Script**. Double-click it when it appears in the list.
4. A text box will appear on the right. Delete the word `cat` and paste this line (make sure to change the path to point to your actual file):
   `/usr/bin/python3 /Users/YourName/Documents/deep-work-tracker/deep_work_tracker.py`
5. Go to the top menu bar, click **File** > **Save**, name it "Deep Work Launcher", and save it to your Applications folder.
6. Now, open your Mac's **System Settings**, click on **General**, then click on **Login Items**.
7. Click the **+** button under the "Open at Login" list, find your new "Deep Work Launcher" in the Applications folder, and add it.

### OPTIONAL Step 4: Make A Manual One-Click Button

We are going to make a simple button so you can launch the tracker manually anytime without touching any code.

**For Windows:**

1. Right-click anywhere on your empty desktop background.
2. Select **New** > **Shortcut**.
3. A box will pop up asking for the location. We need to tell it to run Python, and then point it to where you saved the app. Copy and paste this exact line, but **change the path** to match where you saved your folder:
   `pythonw "C:\Users\YourName\Documents\deep-work-tracker\deep_work_tracker.py"`
4. Click **Next**, name the shortcut "Deep Work", and click **Finish**.
5. **Done!** You can now double-click that icon on your desktop to launch the tracker anytime. _(Pro-tip: Drag the icon down to your taskbar at the bottom of your screen to pin it there for easy access)._

**For Mac:**
Since you already created the "Deep Work Launcher" app in Step 3, you are basically done!

1. Open your **Applications** folder.
2. Find the **Deep Work Launcher** app you made earlier.
3. Click and drag it down to your **Dock** (the bar at the bottom of your screen) or onto your Desktop.
4. **Done!** You now have a one-click button to start your timer manually.

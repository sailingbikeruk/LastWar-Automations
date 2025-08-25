'''
In this script, I am learning/testing how to launch
windows apps
and
android apps (using ADB)

I continue to learn more about creating and using a class.
'''
from EmulatorController import EmulatorController
import pyautogui
import subprocess
import pygetwindow as gw
import win32gui
import win32process
import psutil
import time


window_title="Sailing"

def find_pid_by_window_title(title):
    def callback(hwnd, pid_list):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if window_title == title:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                pid_list.append(pid)
    pid_list = []
    win32gui.EnumWindows(callback, pid_list)
    return pid_list

emulator = EmulatorController()
print("Launching Bluestacks Instance 1 \(Sailing\)")
subprocess.Popen(["C:\Program Files\BlueStacks_nxt\HD-Player.exe", "--instance", "Pie64_1"])
# wait for it to load
print("waiting")
time.sleep(10)
# Connect ADB to Bluestacks
print("connecting to emulator")
emulator.connect_device()

try:
    print("Attempting to start Last War: Survival")
    result = emulator.run_app("com.fun.lastwar.gp")
    print("App Launched")
    print(result)
except subprocess.CalledProcessError as e:
    print("Failed to launch")
    print(e.stderr)
'''
window = gw.getWindowsWithTitle("Sailing")
if window:
    window[0].close()
    time.sleep(2)
    # Example: Click 'Don't Save' at specific screen coordinates
    pyautogui.click(x=1100, y=562)

    print(f"Window '{window_title}' closed.")
else:
    print(f"No window found with title: {window_title}")

pyautogui.screenshot("debug_view.png")
'''

# Find PID(s) for windows with title "Sailing"
pids = find_pid_by_window_title(window_title)

# Gracefully terminate each process
for pid in pids:
    try:
        proc = psutil.Process(pid)
        print(f"Attempting graceful termination: {proc.name()} (PID: {pid})")
        proc.terminate()  # Sends SIGTERM
        proc.wait(timeout=5)  # Wait up to 5 seconds
        print(f"Process {pid} terminated successfully.")
    except psutil.TimeoutExpired:
        print(f"Process {pid} did not terminate in time. Forcing kill.")
        proc.kill()
    except Exception as e:
        print(f"Error terminating")

# This is my main python project file
# It is used to capture screenshots from a particular screen
# in the Android game Last War
# it is run in task scheduler locally

#TODO
# 1. start the program and app so they don't have to be open 24/7 (see launcher.py)
# 2. use a loop to get the second screen if possible rather than repeating the calls to functions
# 3. find a way to ensure you are on the start screen before issuing commands and have returned there when finished
# 4. Add more error checking
# 5. email or SMS on error

from EmulatorController import EmulatorController
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import pygetwindow as gw
import win32process
import subprocess
import pyautogui
import mss.tools
import requests
import datetime
import win32gui
import psutil
import mss
import time
import os
import sys

# Load variable values from .env
load_dotenv()

# set some variables/constants
window_title = "Sailing"
output_dir = "E:\OneDrive\Pictures\LastWar\BotShots"
timestamp_raw = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_filename = f"capture_tech_donations{timestamp_raw}.png"
emulator = EmulatorController()
status_message = "Daily screenshot uploaded successfully ✅"
webhook_url = os.getenv("DISCORD_URL")

#emulator function to show a countdown in the console to I can track timings
def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\rSleeping... {remaining} sec remaining")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rSleep finished.                 \n")
    sys.stdout.flush()

# a function to close the window when all is finished
def close_window(window_title):
    window = gw.getWindowsWithTitle(window_title)
    if window:
        window[0].close()
        time.sleep(2)
        # Example: Click 'Don't Save' at specific screen coordinates
        pyautogui.click(x=1100, y=562)

        print(f"Window '{window_title}' closed.")
    else:
        print(f"No window found with title: {window_title}")

# A function to capture a region of the screen
def capture_screen():
    window = gw.getWindowsWithTitle(window_title)[0]
    print(window)
    left, top, right, bottom = window.left, window.top, window.right, window.bottom
    width = right - left
    height = bottom - top
    with mss.mss() as sct:
        monitor = {
            "left": left,
            "top": top,
            "width": width,
            "height": height
        }
        img = sct.grab(monitor)
        mss.tools.to_png(img.rgb, img.size, output=file_path)

    # Step 4: Overlay timestamp using Pillow
    img = Image.open(file_path)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.rectangle(((10, 10), (280, 40)), fill="black")
    draw.text((15, 13), timestamp, font=font, fill="white")
    img.save(file_path)

# A function to upload files using a discord webhook
def upload_image():
    with open(file_path, 'rb') as f:
        response = requests.post(webhook_url, files={'file': f})

    # Step 5: Send status message
    if response.status_code == 200:
        print("Upload successful. Cleaning up local file.")
        os.remove(file_path)
    else:
        error_msg = f"Screenshot upload failed ❌ Status: {response.status_code}"
        requests.post(webhook_url, json={"content": error_msg})

def open_emulator(package_name):
    emulator = EmulatorController()
    print("Launching Bluestacks Instance 1 - Sailing - (func open-emulator)")
    subprocess.Popen(["C:\Program Files\BlueStacks_nxt\HD-Player.exe", "--instance", "Pie64_1"])
    # wait for it to load
    print("waiting (func open-emulator)")
    countdown_timer(15)
    # Connect ADB to Bluestacks
    print("connecting to emulator (func open-emulator)")
    emulator.connect_device()

    try:
        print("Attempting to start Last War: Survival (func open-emulator)")
        result = emulator.run_app(package_name)
        print("App Launched (func open-emulator)")
        print(result)
    except subprocess.CalledProcessError as e:
        print("Failed to launch (func open-emulator)")
        print(e.stderr)

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

# Ensure output directory exists
print("Checking if image directory exists")
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, screenshot_filename)

#Step 1: Open Bluestacks and Last War
print("Opening emulator and starting last War (main)")
open_emulator("com.fun.lastwar.gp")
print("Waiting for app launch to complete (main)")
countdown_timer(60)


# Step 2: connect ADB to the emulator
if emulator.connect_device():
    print("Connected")
    # if emulator.set_resolution(1920, 1080):
    #    print("Successfully set resolution")

# Step 3: send random clicks on an empty space to clear adverts
    print("Clearing adverts")
    for i in range(5):
        emulator.click_button(1590,90)
        time.sleep(0.5)

# Step 4: Navigate to Alliance tech Donations
    print("Clicking Alliance Button")
    emulator.click_button(1870,760)
    time.sleep(3)

    print("Clicking Alliance Tech Button ")
    emulator.click_button(1100, 690)
    countdown_timer(3)


    print("Clicking Tech Donations Button")
    emulator.click_button(1180, 787)
    countdown_timer(3)
else:
    print("Failed to connect")

# Step 5: Capture the screen region using MSS
print("Capturing positions 1-5")
capture_screen()

# Step 6: Upload screenshot to Discord
print("Uploading positions 1-5")
#upload_image()

#Step 7: scroll to next screen
print("Scolling to positions 6-10")
if emulator.connect_device():
    print("Connected")
    # if emulator.set_resolution(1920, 1080):
    #    print("Successfully set resolution")
    print("Attempting to scroll down")
    emulator.scroll_down(500,700,500,255,1100)

else:
    print("Failed to connect")

#Step 8: Take second capture
countdown_timer(2)
print("Capturing positions 6-10")
capture_screen()

# Step 9: upload second image
print("uploading positions 6-10")
#upload_image()

'''
I tried here to find the close button and click it but I could not get that to work 
so moved to the next code block using PSUTILS

#Step 10: close the bluestacks window
close_window(window_title)
countdown_timer(2)

# Locate the button (requires screenshot of button, e.g. 'close_button.png')
location = pyautogui.locateOnScreen('Close_Sailing.png')

if location:
    # Get center of the button and click
    center_point = pyautogui.center(location)
    pyautogui.click(center_point)
    print("Button clicked!")
else:
    print("Button not found.")
'''
#Step 10: Close Bluestacks
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


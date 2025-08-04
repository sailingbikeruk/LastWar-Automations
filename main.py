# This is my main python project file
# It is used to capture screenshots from a particular screen
# in the Android game Last War
# it is run in task scheduler locally

#TODO
# 1. start the program and app so they dotn have to be open 24/7 (see launcher.py)
# 2. use a loop to get the second screen if possible rather than repeating tehe calls to functions
# 3. find a way to ensure you are on the start screen before issuing commands and have returned there when finished
# 4. Add more error checking
# 5. email or SMS on error

from dotenv import load_dotenv
import pygetwindow as gw
import mss
import mss.tools
from PIL import Image, ImageDraw, ImageFont
import requests
import datetime
import os
from EmulatorController import EmulatorController
import time

from dotenv import load_dotenv
load_dotenv()

# set some variables/constants
window_title = "Sailing"
output_dir = "E:\OneDrive\Pictures\LastWar\BotShots"
timestamp_raw = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_filename = f"capture_tech_donations{timestamp_raw}.png"
emulator = EmulatorController()
status_message = "Daily screenshot uploaded successfully ✅"
webhook_url = os.getenv("DISCORD_URL")

# Define a function to capture a screenshot
# I get the window in #Step 1 below using getWindowsWithTitle() and pass the location to MSS
# I am using MSS because the screen is often on a second of third monitor
# I tiemstamp the images so when they upload its obvious what date and time they are from
def capture_screen():
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

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, screenshot_filename)

# Step 1: Get the window position usign the widnow title to identify it
window = gw.getWindowsWithTitle(window_title)[0]
left, top, right, bottom = window.left, window.top, window.right, window.bottom
width = right - left
height = bottom - top

# Step 2: Move to the right screen inside the game itself
if emulator.connect_device():
    print("Connected")
    # if emulator.set_resolution(1920, 1080):
    #    print("Successfully set resolution")

    print("Clicking Alliance Button")
    emulator.click_button(1870,760)
    time.sleep(3)

    print("Clicking Alliance Tech Button ")
    emulator.click_button(1100, 690)
    time.sleep(3)

    print("Clicking Tech Donations Button")
    emulator.click_button(1180, 787)
    time.sleep(3)
else:
    print("Failed to connect")

# Step 3: Capture the screen region using MSS
print("Capturing positions 1-5")
capture_screen()

# Step 4: Upload screenshot to Discord
print("Uploading positions 1-5")
upload_image()

#Step 6: scroll to next screen
print("Scolling to positions 6-10")
if emulator.connect_device():
    print("Connected")
    # if emulator.set_resolution(1920, 1080):
    #    print("Successfully set resolution")
    print("Attempting to scroll down")
    emulator.scroll_down(500,700,500,255,1000)

else:
    print("Failed to connect")

#Step 7: Take second capture
time.sleep(2)
print("Capturing positions 6-10")
capture_screen()

# Step 8: upload second image
print("uploading positions 6-10")
upload_image()

#Step 9: Go back to base
emulator.send_escape()
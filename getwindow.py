from PIL import ImageGrab
import pygetwindow as gw
import time


# Replace 'Notepad' with the title of the window you want to capture
window_title = 'Sailing'

try:
    # Get the window object by its title
    target_window = gw.getWindowsWithTitle(window_title)[0]

    if target_window:
        # Activate the window to ensure it's in focus (optional, but can help)
        target_window.activate()
        time.sleep(0.5) # Give the window time to become active

        # Get the bounding box coordinates of the window
        # Adjust for potential window borders/shadows if necessary
        bbox = (target_window.left, target_window.top,
                target_window.left + target_window.width,
                target_window.top + target_window.height)

        # Capture the screenshot of the specified region
        screenshot = ImageGrab.grab(bbox=bbox)

        # Save the screenshot
        screenshot.save(f'E:\\OneDrive\\Pictures\\LastWar\\BotShots\\{window_title}.png')
        print(f"Screenshot of 'E:\\OneDrive\\Pictures\\LastWar\\BotShots\\{window_title}.png' saved successfully.")
    else:
        print(f"Window with title '{window_title}' not found.")

except IndexError:
    print(f"Window with title '{window_title}' not found. Make sure it's open.")
except Exception as e:
    print(f"An error occurred: {e}")

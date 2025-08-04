import pygetwindow as gw
import mss
import mss.tools
import os
import pygetwindow as gw
import mss.tools
import os

# window title
window_title="Sailing"

# Get the window
window = gw.getWindowsWithTitle(window_title)[0]
window.restore()
window.activate()

# Define region based on window geometry
region = {
    "top": window.top,
    "left": window.left,
    "width": window.width,
    "height": window.height
    }

# Capture with mss
with mss.mss() as sct:
    img = sct.grab(region)
    mss.tools.to_png(img.rgb, img.size, output="E:\\OneDrive\\Pictures\\LastWar\\BotShots\window_capture.png")

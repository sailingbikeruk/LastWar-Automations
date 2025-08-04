import mss
import pygetwindow as gw
import requests

def capture ():
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

def uplaod():
    webhook_url = 'https://discord.com/api/webhooks/1401570205523640410/eSuuiNiNPNd4P0Rl_6N2WxS9lbGRPlCaToTk64MBg9nY_lMIiJYu6aJHRieaeAkdLzHl'
    file_path = 'E:\OneDrive\Pictures\LastWar\BotShots\window_capture.png'

    with open(file_path, 'rb') as f:
        response = requests.post(webhook_url, files={'file': f})

    if response.status_code == 204:
        print("Upload successful!")
    else:
        print(f"Upload failed: {response.status_code}")

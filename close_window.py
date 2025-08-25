import pyautogui
import pygetwindow as gw
from pynput import mouse

'''
def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")

# Start listening
with mouse.Listener(on_click=on_click) as listener:
    print("Listening for mouse clicks... Press Ctrl+C to stop.")
    listener.join()
'''

window_name="Sailing"
w=gw.getWindowsWithTitle(window_name)[0]
tuple(w.size)

print(w.left)
print(w.bottom)
print(w.width)
print(w.height)


#close_button = pyautogui.locateOnScreen('Close_Sailing2.png', region=(w.left, w.top,w.width,w.height ))
#print(close_button)

pyautogui.screenshot('my_screenshot.png',region=(w.left, w.top,w.width,w.height ))




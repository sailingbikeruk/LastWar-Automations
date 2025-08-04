# This was me playing with button clicks in a simple script

from EmulatorController import EmulatorController
import time

emulator = EmulatorController()

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

    print("Attempting to scroll down")
    emulator.scroll_down(500,700,500,255,1000)
else:
    print("Failed to connect")
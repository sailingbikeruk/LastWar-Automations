'''
In this script, I am learning/testing how to launch
windows apps
and
android apps (using ADB)

I continue to learn more about creating and using a class.
'''
from EmulatorController import EmulatorController
import subprocess
import time

emulator = EmulatorController()
print("Launching Bluestacks Instance 1 \(Sailing\)")
subprocess.Popen(["C:\Program Files\BlueStacks_nxt\HD-Player.exe", "--instance", "Pie64_1" ])
#wait for it to load
print("waiting")
time.sleep(10)
# Connect ADB to Bluestacks
print("connectign to emulator")
emulator.connect_device()

try:
    print("Attempting to start Last War: Survival")
    result=emulator.run_app("com.fun.lastwar.gp")
    print("App Launched")
    print(result)
except subprocess.CalledProcessError as e:
    print("Failed to launch")
    print(e.stderr)
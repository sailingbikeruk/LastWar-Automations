# Credit goes to @software-evolution for ther majority pf this file
# This is a copy of the class file vaguely discussed in this video https://www.youtube.com/watch?v=jcrbnhj3HSU
# I manually copied and typed the code as the author did not supply a downloadable version and I wanted to work through his tutorial
# There are now additional methods that I have added.

import subprocess

class EmulatorController:
    def __init__(self, adb_path='c:\\Android_Tools\\adb.exe', device_ip='127.0.0.1:5565'):
        self.adb_path = adb_path
        self.device_ip = device_ip
        self.device_serial = None

    def connect_device(self):
        result = subprocess.run([self.adb_path, 'connect', self.device_ip], capture_output=True, text=True)
        if 'connected' in result.stdout:
            print("Connected to device")
            devices_result = subprocess.run([self.adb_path, 'devices'], capture_output=True, text=True)
            devices = [line.split()[0] for line in devices_result.stdout.splitlines() if '\tdevice' in line]
            if devices:
                self.device_serial = devices[0]
                print(f"Using device: {self.device_serial}")
                return True
            else:
                print("No devices found")
                return false
        else:
            print("Failed to connect to device")
            return False

    def find_package_name(self, package_name):
        result = subprocess.run([self.adb_path, '-s', self.device_serial, 'shell', 'pm', 'list', 'packages', package_name],capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if package_name in line: # Examnple line: package:com.example.package1
                return line.split(':')[1]
            return None

    def run_app(self,package_name):
        result = subprocess.run([self.adb_path, '-s', self.device_serial, 'shell', 'monkey', '-p', package_name, '-c', 'android.intent.category.LAUNCHER', "1"],check=True, capture_output=True, text=True )
        if result.returncode == 0:
            print(f"Successfully launched the app: {package_name}")
            return True
        else:
            print(f"failed to launch the app:")
            print(f"{result}")
            return False

    def set_resolution(self, width, height):
        if self.device_serial:
            print(f"Setting the resolution to {width}x{height} for device {self.device_serial}")
            result = subprocess.run(
                [self.adb_path, '-s', self.device_serial, 'shell', 'wm', 'size', f'{width}x{height}'],
                text=True,
                capture_output=True
            )
            print("ADB output:", result.stdout)
            print("ADB Error:", result.stdout)
        else:
            print("No device serial specified")

    def click_button(self, x, y):
        if self.device_serial:
            subprocess.run([self.adb_path, '-s', self.device_serial, 'shell', 'input', 'tap', str(x), str(y)])
        else:
            print("No device serial specified")

    def type_text(self, text):
        if self.device_serial:
            escaped_text = text.replace(' ', '%s')
            subprocess.run([self.adb_path, '-s', self.device_serial, 'shell', 'input', 'text', escaped_text])
        else:
            print("No device serial specified")

    def scroll_down(self, start_x, start_y, end_x, end_y, time ):
        if self.device_serial:
            subprocess.run([self.adb_path, '-s', self.device_serial, 'shell', 'input', 'swipe', str(start_x),str(start_y), str(end_x), str(end_y), str(time)])
        else:
            print("No device serial specified")

    def send_escape(self):
        subprocess.run([self.adb_path, '-s', self.device_serial, 'shell', 'input', 'keyevent','111'])

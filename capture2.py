import pygetwindow as gw
import mss
import mss.tools
import os

def capture_window_by_title(window_title, output_path="screenshot.png"):
    try:
        # Find the window
        window = gw.getWindowsWithTitle(window_title)
        if not window:
            print(f"❌ No window found with title: {window_title}")
            return False

        target = window[0]
        left, top, right, bottom = target.left, target.top, target.right, target.bottom
        width = right - left
        height = bottom - top

        # Use MSS to capture the region
        with mss.mss() as sct:
            monitor = {
                "left": left,
                "top": top,
                "width": width,
                "height": height
            }
            img = sct.grab(monitor)
            mss.tools.to_png(img.rgb, img.size, output=output_path)
            print(f"✅ Screenshot saved to {output_path}")
            return True

    except Exception as e:
        print(f"🔥 Error during capture: {e}")
        return False
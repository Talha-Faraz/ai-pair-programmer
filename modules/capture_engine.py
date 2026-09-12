import mss
from PIL import Image
import os
import Quartz

class WindowCapturer:
    def __init__(self):
        self.sct = mss.mss()
        self.temp_dir = "temp_assets"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def get_open_windows(self):
        windows = []
        window_list = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements,
            Quartz.kCGNullWindowID
        )
        for win in window_list:
            app_name = win.get(Quartz.kCGWindowOwnerName, '')
            window_title = win.get(Quartz.kCGWindowName, '')
            if app_name and app_name not in ["Window Server", "Control Center", "Dock"]:
                display_name = f"{app_name}: {window_title}" if window_title else app_name
                if display_name not in windows:
                    windows.append(display_name)
        return sorted(list(set(windows)))

    def capture_target_window(self, target_app_name):
        try:
            window_list = Quartz.CGWindowListCopyWindowInfo(
                Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements,
                Quartz.kCGNullWindowID
            )
            for win in window_list:
                app_name = win.get(Quartz.kCGWindowOwnerName, '')
                window_title = win.get(Quartz.kCGWindowName, '')
                display_name = f"{app_name}: {window_title}" if window_title else app_name
                
                if display_name == target_app_name:
                    bounds = win.get(Quartz.kCGWindowBounds)
                    monitor_region = {
                        "top": int(bounds['Y']),
                        "left": int(bounds['X']),
                        "width": int(bounds['Width']),
                        "height": int(bounds['Height'])
                    }
                    sct_img = self.sct.grab(monitor_region)
                    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                    save_path = os.path.join(self.temp_dir, "current_view.png")
                    img.save(save_path)
                    return save_path
            return f"Error: Window '{target_app_name}' not found."
        except Exception as e:
            return f"Error capturing window: {str(e)}"
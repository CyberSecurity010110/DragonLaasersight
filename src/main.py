import tkinter as tk
from tkinter import colorchooser, Scale
import keyboard
import json
import os
from colorsys import rgb_to_hsv, hsv_to_rgb
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class LaserDot:
    def __init__(self):
        print("Initializing LaserDot...")
        self.config_file = "laser_dot_config.json"
        self.load_config()  # This will now work with the method defined below
        
        try:
            self.root = tk.Tk()
            self.root.title("Laser Dot")
            print("Created main window")
            
            # Make window transparent and frameless
            self.root.attributes('-alpha', 1.0, '-topmost', True)
            self.root.overrideredirect(True)
            self.root.wm_attributes('-transparentcolor', '#000000')
            
            # Get screen dimensions
            self.screen_width = self.root.winfo_screenwidth()
            self.screen_height = self.root.winfo_screenheight()
            print(f"Screen dimensions: {self.screen_width}x{self.screen_height}")
            
            # Create control panel window
            self.control_panel = tk.Toplevel(self.root)
            self.control_panel.title("Laser Dot Controls")
            self.control_panel.geometry("300x400")
            self.control_panel.transient(self.root)
            self.control_panel.attributes('-topmost', True)
            print("Created control panel")
            
            self.setup_control_panel()
            
            # Create canvas for the dot
            self.canvas = tk.Canvas(
                self.root, 
                width=self.screen_width, 
                height=self.screen_height, 
                highlightthickness=0, 
                bg='#000000'
            )
            self.canvas.pack()
            
            self.create_dot()
            print("Created dot")
            
            # Bind hotkeys
            keyboard.on_press_key("f9", lambda _: self.toggle_visibility())
            keyboard.on_press_key("f10", lambda _: self.change_color())
            keyboard.on_press_key("esc", lambda _: self.save_and_quit())
            print("Bound hotkeys")
            
            # Call the window to the front every second
            self.call_to_front()

        except Exception as e:
            print(f"Error during initialization: {str(e)}")
            raise

    def load_config(self):
        print("Loading configuration...")
        default_config = {
            "dot_size": 15,
            "dot_color": "#0000FF",  # Blue
            "opacity": 0.7,
            "brightness": 1.0,
            "visible": True
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = {**default_config, **json.load(f)}
            else:
                self.config = default_config
            print("Configuration loaded successfully")
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            self.config = default_config

    def save_config(self):
        print("Saving configuration...")
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f)
            print("Configuration saved successfully")
        except Exception as e:
            print(f"Error saving config: {str(e)}")

    def setup_control_panel(self):
        # Opacity slider
        tk.Label(self.control_panel, text="Opacity:").pack(pady=5)
        self.opacity_slider = Scale(
            self.control_panel,
            from_=0.1,
            to=1.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.update_opacity
        )
        self.opacity_slider.set(self.config["opacity"])
        self.opacity_slider.pack(pady=5)
        
        # Brightness slider
        tk.Label(self.control_panel, text="Brightness:").pack(pady=5)
        self.brightness_slider = Scale(
            self.control_panel,
            from_=0.1,
            to=1.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.update_brightness
        )
        self.brightness_slider.set(self.config["brightness"])
        self.brightness_slider.pack(pady=5)
        
        # Size slider
        tk.Label(self.control_panel, text="Size:").pack(pady=5)
        self.size_slider = Scale(
            self.control_panel,
            from_=5,
            to=50,
            orient=tk.HORIZONTAL,
            command=self.update_size
        )
        self.size_slider.set(self.config["dot_size"])
        self.size_slider.pack(pady=5)
        
        # Color button
        tk.Button(
            self.control_panel,
            text="Change Color",
            command=self.change_color
        ).pack(pady=10)
        
        # Visibility toggle
        tk.Button(
            self.control_panel,
            text="Toggle Visibility",
            command=self.toggle_visibility
        ).pack(pady=10)
        
        # Hotkey information
        tk.Label(self.control_panel, 
                text="Hotkeys:\nF9: Toggle Visibility\nF10: Change Color\nESC: Save and Quit",
                justify=tk.LEFT).pack(pady=10)

    def create_dot(self):
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        self.dot = self.canvas.create_oval(
            center_x - self.config["dot_size"],
            center_y - self.config["dot_size"],
            center_x + self.config["dot_size"],
            center_y + self.config["dot_size"],
            fill=self.config["dot_color"],
            outline=self.config["dot_color"]
        )
        self.update_opacity(self.config["opacity"])

    def update_opacity(self, value):
        self.config["opacity"] = float(value)
        self.root.attributes('-alpha', self.config["opacity"])

    def update_brightness(self, value):
        self.config["brightness"] = float(value)
        color = self.config["dot_color"]
        r = int(color[1:3], 16) / 255.0
        g = int(color[3:5], 16) / 255.0
        b = int(color[5:7], 16) / 255.0
        h, s, v = rgb_to_hsv(r, g, b)
        r, g, b = hsv_to_rgb(h, s, float(value))
        bright_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        self.canvas.itemconfig(self.dot, fill=bright_color, outline=bright_color)

    def update_size(self, value):
        self.config["dot_size"] = int(value)
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        self.canvas.coords(
            self.dot,
            center_x - self.config["dot_size"],
            center_y - self.config["dot_size"],
            center_x + self.config["dot_size"],
            center_y + self.config["dot_size"]
        )

    def toggle_visibility(self):
        self.config["visible"] = not self.config["visible"]
        if self.config["visible"]:
            self.canvas.itemconfig(self.dot, state='normal')
        else:
            self.canvas.itemconfig(self.dot, state='hidden')

    def change_color(self):
        color = colorchooser.askcolor(title="Choose dot color")[1]
        if color:
            self.config["dot_color"] = color
            self.canvas.itemconfig(self.dot, fill=color, outline=color)
            self.update_brightness(self.brightness_slider.get())

    def save_and_quit(self):
        self.save_config()
        self.root.quit()

    def run(self):
        print("Starting main loop...")
        self.root.mainloop()

    def call_to_front(self):
        self.root.attributes('-topmost', True)
        self.root.after(1000, self.call_to_front)  # Call this method every second

def main():
    if not is_admin():
        print("Requesting admin privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return

    print("Starting LaserDot application...")
    try:
        laser = LaserDot()
        print("LaserDot instance created successfully")
        print("Running main loop...")
        laser.run()
    except Exception as e:
        print(f"Error: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()

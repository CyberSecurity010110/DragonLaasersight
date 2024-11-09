# src/main.py

import ctypes
import sys
from laser_dot import LaserDot, is_admin

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

# DragonLaserSight

DragonLaserSight is a Python application for managing and controlling a laser dot overlay on your screen with advanced features.
Features

    Change dot size, color, opacity, and brightness
    Toggle visibility
    Hotkeys for quick access
    Configuration persistence

    #This version is free, a contribution to the open source community which has given me so much, however, I have made a much more detailed version with,
     A pulsing breathing effect effect, a rainbow color changinging effect, 2 dozen crosshairs that have the same options as the dot and are seperately configured so if you 
     wanted a rainbow color changing crosshair and red see thru pulsing dot of different sizes for example, its doable. I can also likly add any features requested.
     If you want this enhanced version, pm me at privesec010110@gmail.com or jedidragonsurfer@gmail.com

# Installation

    Clone the repository:

    git clone https://github.com/Cybersecurity010110/DragonLaserSight.git
    cd DragonLaserSight

    Install the required Python packages:

bash

pip install -r requirements.txt

# Usage

Run the main script:

bash

python src/main.py
Building the Executable

To create an executable from the source code, follow these steps:

    Ensure you have pyinstaller installed. If not, you can install it using pip:

    pip install pyinstaller

    Navigate to the root directory of the project:

bash

cd path/to/your/project

Run the following command to create the executable:

bash

pyinstaller --onefile --windowed src/main.py


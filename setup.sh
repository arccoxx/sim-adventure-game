
#!/bin/bash

cd "$(dirname "$0")"
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py 
pip install pygame
pip install pygame_gui
python3 -m pip install -U pygame --user
python3 game.py


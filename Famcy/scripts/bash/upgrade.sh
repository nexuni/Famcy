#!/bin/bash
cd ~/.local/share/famcy/$2
source venv/bin/activate
pip3 install famcy --upgrade

echo "Famcy Upgrade Finished..."
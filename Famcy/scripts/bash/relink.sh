#!/bin/bash
cd ~/.local/share/famcy/$2
source venv/bin/activate
pip3 install famcy --upgrade
cd $1
ln -s ~/.local/share/famcy/$2/console/ _CONSOLE_FOLDER_

cd static
ln -s ~/.local/share/famcy/$2/console/_static_/user_css/ user_css
ln -s ~/.local/share/famcy/$2/console/_static_/user_js/ user_js
ln -s ~/.local/share/famcy/$2/console/_static_/user_image/ user_image

echo "Famcy Upgrade Finished..."
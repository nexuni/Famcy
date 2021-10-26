#!/bin/bash
source ~/.local/share/famcy/$2/venv/bin/activate
cd $1
export FLASK_APP="app:create_app('$2', True)"
flask run

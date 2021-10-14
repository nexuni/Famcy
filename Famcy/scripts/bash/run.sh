#!/bin/bash
source ~/.local/share/famcy/$2/venv/bin/activate
cd $1
flask run

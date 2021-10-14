#!/bin/bash
if ! hash python3; then
    echo "python is not installed"
    exit 1
fi

ver=$(python3 -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "37" ]; then
    echo "Famcy requires python 3.7 or greater"
    exit 1
fi

mkdir -p ~/.local/share/famcy/$1
cd ~/.local/share/famcy/$1
python3 -m venv venv
source venv/bin/activate
pip3 install wheel uwsgi
pip3 install setuptools-rust
pip3 install famcy

dir="console"
if [ -d "$dir" -a ! -h "$dir" ]
then
	echo "$dir found and not pulling famcy console template from cloud"
else
	echo "Initializing new famcy template..."
	wget https://gadgethi-css.s3.amazonaws.com/FamcyConsole.zip
	tar -xf FamcyConsole.zip
	mv FamcyConsole console
	rm FamcyConsole.zip
fi


#!/bin/bash
#get path to script
DIR=$PWD/$(dirname $0)
#copy script
cp  $DIR/check4sound.py  ~/check4sound.py
#create virtual environment
python3 -m venv ~/.venv
source ~/.venv/bin/activate
pip install -r $DIR/requirements.txt
#install supervisor
sudo apt install -y supervisor
sudo cp $DIR/soundcheck.conf /etc/supervisor/conf.d/soundcheck.conf
sudo service supervisor restart
sudo supervisorctl status

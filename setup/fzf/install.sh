#!/bin/bash
sudo apt install fzf -y
DIR=$PWD/$(dirname $0)
if grep -Fq "fzf.bash" ~/.bashrc
then
    cat ~/.bashrc
else
    echo "[ -f $DIR/fzf.bash ] && source $DIR/fzf.bash" >> ~/.bashrc
fi

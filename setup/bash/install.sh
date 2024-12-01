#!/bin/bash
DIR=$PWD/$(dirname $0)
if grep -Fq "alias.bash" ~/.bashrc
then
    cat ~/.bashrc
else
    echo "[ -f $DIR/alias.bash ] && source $DIR/alias.bash" >> ~/.bashrc
fi

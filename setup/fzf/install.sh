#!/bin/bash
#sudo apt install fzf -y #outdated
git clone --depth 1 https://github.com/junegunn/fzf.git $HOME/src/fzf
$HOME/src/fzf/install --key-bindings --completion --no-update-rc
sudo cp $HOME/src/fzf/bin/fzf /usr/local/bin
DIR=$PWD/$(dirname $0)
if grep -Fq "fzf.bash" ~/.bashrc
then
    cat ~/.bashrc
else
    echo "[ -f $DIR/fzf.bash ] && source $DIR/fzf.bash" >> ~/.bashrc
fi

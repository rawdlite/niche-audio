#!/bin/bash
#get path to script
DIR=$PWD/$(dirname $0)
curl https://sh.rustup.rs -sSf | sh
# compile cargo
mkdir ~/.cargo/tmp
export CARGO_TARGET_DIR=~/.cargo/tmp
export CARGO_INSTALL_ROOT=/usr/local
cargo install --locked zellij
mkdir ~/.config/zellij
ln -s $DIR/config.kdl ~/.config/zellij/config.kdl
if grep -Fq "zellij.bash" ~/.bashrc
then
    cat ~/.bashrc
else
    echo "[ -f $DIR/zellij.bash ] && source $DIR/zellij.bash" >> ~/.bashrc
fi

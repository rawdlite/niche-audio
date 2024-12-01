#!/bin/bash
# reduce dependencies an make option for basic install
sudo apt install mpv fd-find golang flac -y
# update go 
# dietpi-software reinstall 188
export GOPATH=/usr/local
env CGO_ENABLED=0 go install -ldflags="-s -w" github.com/gokcehan/lf@latest
mkdir /etc/lf
ln -s /root/src/niche-audio/setup/lf/lfrc /etc/lf/lfrc
mkdir -p ~/.cargo/tmp
export CARGO_TARGET_DIR=~/.cargo/tmp
export CARGO_INSTALL_ROOT=/usr/local
#get path to script
DIR=$PWD/$(dirname $0)
#sudo apt install mpv flac -y
# install run-mailcap-rs
#mkdir ~/src
git clone https://github.com/cglindkamp/run-mailcap-rs.git ~/src/run-mailcap-rs
#cd ~/src/run-mailcap-rs
#cargo install
#make
#sudo make install
#ln -s $DIR/mailcap ~/.mailcap
#ln -s $DIR/scripts/* /usr/local/bin
python3 -m pip install eyeD3
if grep -Fq "lf.bash" ~/.bashrc
then
    cat ~/.bashrc
else
    echo "[[ -f $DIR/lf.bash ]] && source $DIR/lf.bash" >> ~/.bashrc
fi
source ~/.bashrc

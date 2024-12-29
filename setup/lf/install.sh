#!/bin/bash
# reduce dependencies an make option for basic install
sudo apt install less mpv fd-find golang flac -y
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
# install run-mailcap-rs /deprecated not handling symbolic links
mkdir ~/src
#git clone https://github.com/cglindkamp/run-mailcap-rs.git ~/src/run-mailcap-rs
#cd ~/src/run-mailcap-rs
#cargo install
#make
#sudo make install
git clone https://github.com/pld-linux/mailcap.git ~/src/mailcap
sudo cp ~/src/mailcap/mailcap /usr/share/etc
sudo cp ~/stc/mailcap/run-mailcap /usr/local/bin
sudo chmod +x /usr/local/bin/run-mailcap
ln -s $DIR/mailcap ~/.mailcap
ln -s $DIR/scripts/* /usr/local/bin
echo "i quit" >> ~/.config/lesskey
python3 -m pip install eyeD3
if grep -Fq "lf.bash" ~/.bashrc
then
    cat ~/.bashrc
else
    echo "[[ -f $DIR/lf.bash ]] && source $DIR/lf.bash" >> ~/.bashrc
fi
source ~/.bashrc

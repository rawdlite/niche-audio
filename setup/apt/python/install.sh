apt install python3.11-venv
python3 -m venv /root/src/niche-audio/audio-remote/.venv
source /root/src/niche-audio/audio-remote/.venv/bin/activate
pip install gpiozero
pip install pigpio
git clone https://github.com/molobrakos/lms.git /root/src/lms
cd /root/src/lms
python setup.py build
pip install -r requirements.txt
python setup.py install
pip install pigpio_encoder

source /root/src/niche-audio/audio-remote/.venv/bin/activate
git clone https://github.com/rawdlite/niche-audio /root/src/niche-audio
pip install -r /root/src/niche-audio/audio-remote/requirements.txt
git clone https://github.com/molobrakos/lms.git /root/src/lms
cd /root/src/lms
python setup.py build
pip install -r requirements.txt
python setup.py install


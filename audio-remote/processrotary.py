#!/usr/bin/env python3
import tomllib
from pathlib import Path
from lms import Server, __version__
from pigpio_encoder.rotary import Rotary
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306
from PIL import ImageFont, ImageDraw, Image
from urls.LMSURL import URL, Saraswati

with open(Path.home() / ".config" / "niche-audio" / "config.toml", mode="rb") as fp:
    settings = tomllib.load(fp)

SERVER_ID = settings['general']['server']
PLAYERNAME = settings['general']['player']
DEBUG = settings ['general']['debug']
TIMEOUT = settings['rotary']['timeout']
CHOICES = list(URL.keys())
LASTCHOICE = 0
# initialise display
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)
oled_font = ImageFont.truetype('DejaVuSans.ttf', 20)
runtime = 0
server = None
player = None

my_rotary = Rotary(
    clk_gpio=settings['rotary']['clk_pin'],
    dt_gpio=settings['rotary']['dt_pin'],
    sw_gpio=settings['rotary']['sw_pin']
)

sara = Saraswati()

def up_callback(counter):
    if counter >= my_rotary.max:
        my_rotary.counter = 0
        counter = 0 
    display_choice(counter)


def down_callback(counter):
    if counter <= -1:
        my_rotary.counter = my_rotary.max - 1
        counter = my_rotary.max - 1
    display_choice(counter)


def sw_short():
    global loop
    counter = my_rotary.counter
    if counter <= -1:
        counter = 0
    display_choice(counter)
    play_choice(counter)


def sw_long():
    display("Switch long press")


my_rotary.setup_rotary(
    min=-1,
    max=len(CHOICES),
    scale=1,
    #  debounce=2,
    #  rotary_callback=rotary_callback,
    up_callback=up_callback,
    down_callback=down_callback
)

my_rotary.setup_switch(
    debounce=200,
    long_press=True,
    sw_short_callback=sw_short,
    sw_long_callback=sw_long
)


def display(text):
    with canvas(device) as draw:
        # draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((5, 20), text, font=oled_font, fill="white")

def display_choice(counter):
    global runtime
    runtime = 0
    device.show()
    with canvas(device) as draw:
        draw.text((5, 20), CHOICES[counter], font=oled_font, fill="white")

def play_choice(counter):
    global server
    global player
    url = sara.get_url(CHOICES[counter])
    if not server:
        server = Server(SERVER_ID)
        server.update()
    if not player:
        player = (next((player for player in server.players
                        if PLAYERNAME.lower() in [
                            player.player_id,
                            player.name.lower(),
                            player.ip]), None)
                  if PLAYERNAME else None)
    #remote.send('power')
    if DEBUG:
        print(f"url: {url}")
    if type(url) == list:
        player.query(*url)
        player.play()
    else:
        player.play_uri(url)
            

def main():
    global runtime
    display("turn me on")
    time.sleep(2)
    while True:
        runtime += 1
        time.sleep(0.5)
        if runtime >= TIMEOUT:
            device.hide()


if __name__ == '__main__':
    main()

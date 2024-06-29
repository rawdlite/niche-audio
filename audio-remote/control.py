#!/usr/bin/env python3
from pysqueezebox import Server, Player
import aiohttp
import asyncio
from pigpio_encoder.rotary import Rotary
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306
from PIL import ImageFont, ImageDraw, Image
from urls.LMSURL import URL, Saraswati

SERVER = 'dietpi5.fritz.box' # ip address of Logitech Media Server
PLAYERNAME = 'Moode'
TIMEOUT = 120
CHOICES = list(URL.keys())
LASTCHOICE = 0
# initialise display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
oled_font = ImageFont.truetype('DejaVuSans.ttf', 20)
runtime = 0

my_rotary = Rotary(
    clk_gpio=21,
    dt_gpio=20,
    sw_gpio=17
)

sara = Saraswati()
loop = asyncio.get_event_loop()

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
    loop.run_until_complete(play_choice(counter))


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

async def play_choice(counter):
    url = sara.get_url(CHOICES[counter])
    print(f"url: {url}")
    async with aiohttp.ClientSession() as session:
        lms = Server(session, SERVER)
        print("got server session")
        player = await lms.async_get_player(name=PLAYERNAME)
        if not player:
            print("failed to get player")
            return
        else:
            print("got player")
        if type(url) == list:
            await player.async_query(*url)
        else:
            await player.async_load_url(url, cmd="load")

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

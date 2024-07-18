#!/usr/bin/env python3
from pysqueezebox import Server, Player
import aiohttp
import asyncio
import argparse
import time
import random
import subprocess
import piir
from gpiozero import LED, PWMLED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause
import subprocess
from urls.LMSURL import URL, Saraswati
factory = PiGPIOFactory()
DEBUG = False
#led_yellow = PWMLED(12, pin_factory=factory)
#led_green = PWMLED(5, frequency=800, pin_factory=factory)
#led_red = PWMLED(6, pin_factory=factory)
print("start")
#led_green.blink()
button_4 = Button(6, pin_factory=factory, bounce_time=0.1)
#button_green = Button(20, pin_factory=factory, bounce_time=0.3)
#button_white = Button(21, pin_factory=factory)
button_1 = Button(13, pin_factory=factory)
button_2 = Button(19, pin_factory=factory)
button_3 = Button(26, pin_factory=factory)

SERVER = '192.168.178.79' # ip address of Logitech Media Server
player_name = 'Moode'
TIMEOUT = 200
remote = piir.Remote('/root/src/niche-audio/piir/rme.json', 18)
parser = argparse.ArgumentParser(
        prog='processbutton',
        description='process button presses to control LMS',
        epilog='uses gpiozero and pigpio')
parser.add_argument('-v', '--verbose',
                    action='store_true')
args = parser.parse_args()
if args.verbose:
    DEBUG=True

async def main():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, SERVER)
        if DEBUG and lms:
            print("got server session")
        player = await lms.async_get_player(name=player_name)
        sara = Saraswati()
        if DEBUG and player:
            print("got player")
        if not player:
            if DEBUG:
                print(f"failed to get player {player_name} from {SERVER}")
            time.sleep(0.5)
            exit(1)
        await player.async_update()
        while True:
            if button_1.is_pressed:
                await player.async_toggle_pause()
                await player.async_update()
                if DEBUG == True:
                    print(player.mode)
            if button_2.is_pressed:
                await player.async_load_url(URL['Radio1'], cmd="load")
                remote.send('power')
                if DEBUG == True:
                    print("button 2")
            if button_3.is_pressed:
                await player.async_query("playlist","jump","2")
            if button_4.is_pressed:
                subprocess.run("/usr/local/bin/rme-power", shell=True)
                #await player.async_load_url(URL['Electro'], cmd="load")
            time.sleep(0.1)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())


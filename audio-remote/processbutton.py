#!/usr/bin/env python3
import tomllib
from pathlib import Path
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
print("start")

with open(Path.home() / ".config" / "niche-audio" / "config.toml", mode="rb") as fp:
    settings = tomllib.load(fp)

SERVER = settings['general']['server']
PLAYERNAME = settings['general']['player']
TIMEOUT = settings['button']['timeout']
button_1 = Button(settings['button']['button_1'], pin_factory=factory, bounce_time=0.1)
button_2 = Button(settings['button']['button_2'], pin_factory=factory)
button_3 = Button(settings['button']['button_3'], pin_factory=factory)
button_4 = Button(settings['button']['button_4'], pin_factory=factory)

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
        player = await lms.async_get_player(name=PLAYERNAME)
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


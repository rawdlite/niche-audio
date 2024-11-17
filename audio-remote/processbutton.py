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
import tomllib
from urls.LMSURL import URL, Saraswati
factory = PiGPIOFactory()
#print("start")

with open(Path.home() / ".config" / "niche-audio" / "config.toml", mode="rb") as fp:
    settings = tomllib.load(fp)

DEBUG = settings['general']['debug']
SERVER = settings['general']['server']
#print(SERVER)
PLAYERNAME = settings['general']['player']
#print(PLAYERNAME)
TIMEOUT = settings['button']['timeout']
button_green1 = Button(settings['button']['button_green1'], 
                       pin_factory=factory, 
                       bounce_time=0.1)
button_yellow1 = Button(settings['button']['button_yellow1'],
                        pin_factory=factory)
button_blue1 = Button(settings['button']['button_blue1'],
                      pin_factory=factory)
button_red1 = Button(settings['button']['button_red1'],
                     pin_factory=factory)
button_green2 = Button(settings['button']['button_green2'], 
                       pin_factory=factory, 
                       bounce_time=0.1)
button_yellow2 = Button(settings['button']['button_yellow2'],
                        pin_factory=factory)
button_blue2 = Button(settings['button']['button_blue2'],
                      pin_factory=factory)
button_red2 = Button(settings['button']['button_red2'],
                     pin_factory=factory)
parser = argparse.ArgumentParser(
        prog='processbutton',
        description='process button presses to control LMS',
        epilog='uses gpiozero and pigpio')
parser.add_argument('-v', '--verbose',
                    action='store_true')
args = parser.parse_args()
if args.verbose:
    DEBUG=True

def show_button(button):
    print(button.pin)

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
            if button_red1.is_pressed:
                await player.async_toggle_pause()
                await player.async_update()
                if DEBUG == True:
                    show_button(button_red1)
                    print(player.mode)
            if button_green1.is_pressed:
                await player.async_load_url(URL['Radio1'], cmd="load")
                if DEBUG == True:
                    print("button 2")
            if button_red2.is_pressed:
                subprocess.run("/root/bin/rme-toggle-power.sh", shell=True)
            if button_yellow2.is_pressed:
                subprocess.run("/root/bin/amp-toggle-power.sh", shell=True)
                #await player.async_load_url(URL['Electro'], cmd="load")
            time.sleep(0.1)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())


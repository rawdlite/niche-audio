#!/usr/bin/python3
import tomllib
from pathlib import Path
from pysqueezebox import Server, Player
import aiohttp
import asyncio
import time
import pirc522
from lcd import LCD1602 as LCD
import random
from gpiozero import LED, PWMLED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from urls.LMSURL import URL, Saraswati
factory = PiGPIOFactory()
DEBUG = True
with open(Path.home() / ".config" / "niche-audio" / "config.toml", mode="rb") as fp:
    settings = tomllib.load(fp)

SERVER = settings['general']['server']
PLAYERNAME = settings['general']['player']
led = PWMLED(settings['rfid']['led'], pin_factory=factory)
led_green = PWMLED(settings['rfid']['led_green'], pin_factory=factory)
led_red = PWMLED(settings['rfid']['led_red'], pin_factory=factory)

factory = PiGPIOFactory()
PIN_IRQ = settings['rfid']['PIN_IRQ']
PIN_RST = settings['rfid']['PIN_RST']


DANCE   = 4073702892
ELEKTRO = 317969388
KRAUT   = 851426028
BLUES   = 4066689772
Inc     = 845529836
K2      = 3529360108
J1      = 3001597676
K1      = 3808146924
S1      = 581030892
BLUE    = 2043527857

#reader = SimpleMFRC522()
reader = pirc522.RFID(pin_mode='BOARD', pin_rst=PIN_RST, pin_irq=PIN_IRQ, antenna_gain=3)
#RETRY = 9
LCD.init(0x27, 1)
TIMEOUT = settings['rfid']['timeout']

def destroy():
    print("cleanup")
    GPIO.cleanup()


async def main():
    async with aiohttp.ClientSession() as session:
        led.blink(on_time=0.1, off_time=0.1)
        lms = Server(session, SERVER)
        sara = Saraswati()
        player = await lms.async_get_player(name=PLAYERNAME)
        #print("got player")
        timeout = TIMEOUT
        await player.async_update()
        rfid_uid = None
        led.off()
        while True:
            led.off()
            #print("waiting")
            reader.wait_for_tag()
            uid = reader.read_id(True)
            if uid is not None and uid != rfid_uid:
                #print(uid)
                rfid_uid = uid
                timeout = TIMEOUT
                led.blink(on_time=0.2, off_time=0.1)
                if uid == BLUES:
                    LCD.write(0,0,"Blues")
                    url = sara.get_url('Blues')
                elif uid == DANCE:
                    LCD.write(0,0,"Dance")
                    url = sara.get_url('dance')
                elif uid == KRAUT:
                    LCD.write(0,0,"Krautrock")
                    url = sara.get_url('Krautrock')
                elif uid == ELEKTRO:
                    LCD.write(0,0,"Electro")
                    url = sara.get_url('Electro')
                elif uid == S1:
                    LCD.write(0,0,"Soul")
                    url = sara.get_url('Soul')
                elif uid == J1:
                    LCD.write(0,0,"Jazz")
                    url = sara.get_url('Jazz')
                if url:
                    if type(url) == list:
                        await player.async_query(*url)
                    else:
                        await player.async_load_url(url, cmd="load")
                    url = None    
            time.sleep(0.5)
            timeout -= 1
            if timeout == 0:
                LCD.closelight()
            #print("running")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

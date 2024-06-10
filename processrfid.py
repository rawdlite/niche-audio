#!/usr/bin/python3
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
led = PWMLED(12, pin_factory=factory)
led_green = PWMLED(5, pin_factory=factory)
led_red = PWMLED(6, pin_factory=factory)

factory = PiGPIOFactory()
PIN_IRQ = 18
PIN_RST = 22


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
TIMEOUT = 200
SERVER = '192.168.178.4' # ip address of Logitech Media Server
player_name = 'RaspdacEvo'

def destroy():
    print("cleanup")
    GPIO.cleanup()


async def main():
    async with aiohttp.ClientSession() as session:
        led.blink(on_time=0.1, off_time=0.1)
        lms = Server(session, SERVER)
        sara = Saraswati()
        player = await lms.async_get_player(name=player_name)
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
                    #await player.async_query("playlist","loadalbum","Blues","John Lee Hooker","*")
                elif uid == DANCE:
                    LCD.write(0,0,"Dance")
                    url = sara.get_url('dance')
                    #await player.async_load_url(URL['dance'], cmd="load")
                elif uid == KRAUT:
                    LCD.write(0,0,"Krautrock")
                    url = sara.get_url('Krautrock')
                elif uid == ELEKTRO:
                    LCD.write(0,0,"Electro")
                    url = sara.get_url('Electro')
                    #print("play Elektro")
                    #await player.async_load_url(URL['electro'], cmd="load")
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

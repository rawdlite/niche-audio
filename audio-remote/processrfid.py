#!/usr/bin/python3
from pysqueezebox import Server, Player
import aiohttp
import asyncio
import time
import pirc522
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
PIN_IRQ = 18
PIN_RST = 22

led = LED(23, pin_factory=factory)

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
SERVER = 'dietpi5.fritz.box' # ip address of Logitech Media Server
player_name = 'Moode'
#url = 'http://open.qobuz.com/playlist/1208967'
URL = {
        'kraut': 'http://open.qobuz.com/playlist/1208967',
        'radio1':  'http://opml.radiotime.com/Tune.ashx?id=s25111&formats=aac,ogg,mp3&partnerId=16&serial=a44d9baf7190744ec4fa880f24a9fdba',
        'dance': 'http://open.qobuz.com/playlist/2722317',
        'electro': 'http://open.qobuz.com/playlist/2561228',
        'ambient': 'http://open.qobuz.com/playlist/21001567',
        'Jazz': [
            'https://open.qobuz.com/playlist/9698201',
            'https://open.qobuz.com/playlist/3484206',
            'https://open.qobuz.com/playlist/9163705',
            'https://open.qobuz.com/playlist/5692098',
            'https://open.qobuz.com/playlist/2561220'
            ],
        'Incomming': 'https://open.qobuz.com/playlist/21711341',
        'Audio Test': [
            'https://open.qobuz.com/playlist/12407647',
            'https://open.qobuz.com/playlist/12308506',
            'https://open.qobuz.com/playlist/9944942'
            ]
        }

def destroy():
    print("cleanup")
    GPIO.cleanup()


async def main():
    async with aiohttp.ClientSession() as session:
        led.on()
        lms = Server(session, SERVER)
        player = await lms.async_get_player(name=player_name)
        if player:
            print("got player")
        else:
            print(f"player {player_name} not found on {SERVER}")
            exit(1)
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
                led.on()
                if uid == BLUES:
                    #print("play Blues")
                    await player.async_query("playlist","loadalbum","Blues","John Lee Hooker","*")
                elif uid == DANCE:
                    #print("play Dance")
                    await player.async_load_url(URL['dance'], cmd="load")
                elif uid == KRAUT:
                    #print("play Kraut")
                    await player.async_load_url(URL['kraut'], cmd="load")
                elif uid == ELEKTRO:
                    #print("play Elektro")
                    await player.async_load_url(URL['electro'], cmd="load")
                elif uid == J1:
                    
                    await player.async_query("playlist","play","Jazz")
                elif uid == STOP:
                    await player.async_stop()
            time.sleep(0.5)
            #print("running")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

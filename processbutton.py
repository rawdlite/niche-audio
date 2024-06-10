#!/usr/bin/env python3
from pysqueezebox import Server, Player
import aiohttp
import asyncio
from lcd import LCD1602 as LCD
import time
import random
from gpiozero import LED, PWMLED, Button
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause
import subprocess
from urls.LMSURL import URL, Saraswati
factory = PiGPIOFactory()
DEBUG = True
led_yellow = PWMLED(12, pin_factory=factory)
led_green = PWMLED(5, frequency=800, pin_factory=factory)
led_red = PWMLED(6, pin_factory=factory)
print("start")
led_green.blink()
button_red = Button(16, pin_factory=factory, bounce_time=0.1)
button_green = Button(20, pin_factory=factory, bounce_time=0.3)
button_white = Button(21, pin_factory=factory)
button_yellow = Button(13, pin_factory=factory)
button_blue = Button(19, pin_factory=factory)
button_black = Button(26, pin_factory=factory)

SERVER = '192.168.178.4' # ip address of Logitech Media Server
player_name = 'RaspDacEvo'
TIMEOUT = 200
LCD.init(0x27, 1)
CHOICES = list(URL.keys())

def show_choice(choice):
    print(CHOICES[choice])
    LCD.write(0,1,CHOICES[choice])


def change_choice(choice,step):
    choice += step
    if choice >= len(CHOICES):
        choice = 0
    elif choice < 0:
        choice = len(CHOICES) - 1
    #print(f"choice: {choice}")
    LCD.write(0,1,CHOICES[choice])
    return choice




async def main():
    led_green.blink()
    async with aiohttp.ClientSession() as session:
        lms = Server(session, SERVER)
        player = await lms.async_get_player(name=player_name)
        choice = len(CHOICES)
        sara = Saraswati()
        timeout = TIMEOUT
        if DEBUG:
            print("got player")
        await player.async_update()
        led_green.off()
        while True:
            if button_red.is_pressed:
                timeout = TIMEOUT
                #print("button RED")
                #LCD1602.write(0,0,"Button Red")
                led_green.blink()
                #await player.async_stop()
                await player.async_toggle_pause()
                await player.async_update()
                LCD.write(0,0,player.mode)
                #if DEBUG == True:
                #    print(player.mode)
            if button_green.is_pressed:
                timeout = TIMEOUT
                #print("button Green")
                #LCD1602.write(0,0,"Button Green")
                led_green.blink()
                await player.async_load_url(URL['radio1'], cmd="load")
                LCD.write(0,0,"Radio 1")
                #if DEBUG == True:
                #    print("button 2")
            if button_white.is_pressed:
                timeout = TIMEOUT
                led_green.blink()
                #print("button White")
                #LCD1602.openlight()
                choice = change_choice(choice,1)
            if button_yellow.is_pressed:
                timeout = TIMEOUT
                led_green.blink()
                await player.async_query("playlist","jump","2")
            if button_blue.is_pressed:
                timeout = TIMEOUT
                #print("button Blue")
                #LCD1602.write(0,0,"Button Blue")
                led_green.blink()
                url = sara.get_url(CHOICES[choice])
                if type(url) == list:
                    await player.async_query(*url)
                else:
                    await player.async_load_url(url, cmd="load")
                #await player.async_load_url(URL[CHOICES[choice]], cmd="load")
            if button_black.is_pressed:
                timeout = TIMEOUT
                #print("button Black")
                #LCD.write(0,0,"Button Black")
                led_green.blink()
                choice = change_choice(choice,-1)
            led_green.off()
            time.sleep(0.1)
            timeout -= 1
            if timeout == 0:
                #LCD1602.clear()
                try:
                    LCD.closelight()
                except:
                    print("close")
            #print("running")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())


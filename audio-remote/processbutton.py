#!/usr/bin/env python3
from gpiozero import Device, Button, ButtonBoard, PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory
import time
import pprint
import tomllib
from pathlib import Path
from signal import pause
import subprocess
import argparse

parser = argparse.ArgumentParser(description='read button input')
parser.add_argument("-v", "--verbose", dest="verbosity", action="count", default=0,
                    help="Verbosity (between 1-2 occurrences with more leading to more "
                         "verbose output") 
args = parser.parse_args()


Device.pin_factory = PiGPIOFactory()

with open(Path.home() / ".config" / "niche-audio" / "config.toml", mode="rb") as fp:
    settings = tomllib.load(fp)

button_config = settings['button_config']
button_actions_sw0 = settings['button_actions_sw0']
button_actions_sw1 = settings['button_actions_sw1']
switch1 = Button(settings['switch']['switch1'])
if args.verbosity > 1:
    pprint.pp(button_actions_sw0,indent=2,sort_dicts=True)
    pprint.pp(button_actions_sw1,indent=2,sort_dicts=True)

led_green = PWMLED(settings['led']['led_green'],
                   active_high=False)
led_red = PWMLED(settings['led']['led_red'],
                 active_high=False)
bb = ButtonBoard(hold_time=3,hold_repeat=False, **button_config)

seperator = "-"

led_red.pulse()
time.sleep(0.5)
led_green.pulse()
time.sleep(5)
led_red.off()
led_green.off()

def say_pressed(butt):
    if switch1.value:
        script = button_actions_sw1[[k for k,v in butt.value._asdict().items() if v == 1][0]]
    else:
        script = button_actions_sw0[[k for k,v in butt.value._asdict().items() if v == 1][0]]
    if args.verbosity > 1:
        print(f"press {butt.value}")
        print(tuple(butt.value))
    if args.verbosity:
        print(script)
    led_green.on()
    try:
        res = subprocess.run(script, shell=True, check=True)
        if args.verbosity > 1:
            print(res)
    except subprocess.CalledProcessError as err:
        print(f"{script} failed {err}")
        pass
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        pass
    finally:
        led_green.off()

def say_held(butt):
    print(butt.value)
    print(int(''.join(str(bit) for bit in tuple(butt.value)), 2))
    butt.wait_for_release(5)

bb.when_pressed = say_pressed
bb.when_held = say_held

pause()

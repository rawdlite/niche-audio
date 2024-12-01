from gpiozero import Device, ButtonBoard, PWMLED
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
button_actions = settings['button_actions']
if args.verbosity > 1:
    pprint.pp(button_actions,indent=2,sort_dicts=True)

led_green = PWMLED(settings['led']['led_green'],
                   active_high=False)
led_red = PWMLED(settings['led']['led_red'],
                 active_high=False)
bb = ButtonBoard(hold_time=3,hold_repeat=False, **button_config)

seperator = "-"

led_red.blink()
led_green.pulse()
time.sleep(4)
led_red.off()
led_green.off()

def say_pressed(butt):
    script = button_actions[[k for k,v in butt.value._asdict().items() if v == 1][0]]
    if args.verbosity > 1:
        print(f"press {butt.value}")
        print(tuple(butt.value))
    if args.verbosity:
        print(script)
    res = subprocess.run(script, shell=True, check=True)
    if args.verbosity > 1:
        print(res)

def say_held(butt):
    print(butt.value)
    print(int(''.join(str(bit) for bit in tuple(butt.value)), 2))
    butt.wait_for_release(5)

bb.when_pressed = say_pressed
bb.when_held = say_held

pause()

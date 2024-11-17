#!/usr/bin/env python3

SOUNDCARD_DEVICE_FILE = "/proc/asound/sndallodigione/pcm0p/sub0/status" # Path of souncard status file
SHUTDOWN_TIMEOUT = 15 # Delay before amplifier power down after soundcard released
DEBUG = False
#---------------------------8--------
import os
import time
import subprocess

deviceFile = None
lastIdle = None

def Now():
    return int(time.time())

def CheckSoundcardStatus():
    global deviceFile
    buf = ""
    lastException = None
    for i in range(3):
        try:
            os.lseek(deviceFile, 0, os.SEEK_SET)
            buf = os.read(deviceFile, 14)
            return (len(buf) == 14 and buf[7] == 82 and buf[8] == 85 and \
                buf[9] == 78 and buf[10] == 78 and buf[11] == 73 and \
                buf[12] == 78 and buf[13] == 71) # Check for "RUNNING"
        except Exception as ex: # Attempt to open device file again
            try:
                os.close(deviceFile)
            except:
                pass
            try:
                deviceFile = os.open(SOUNDCARD_DEVICE_FILE, os.O_RDONLY)
            except Exception as ex:
                lastException = ex
    raise lastException # All attempt failed


def PowerOn():
    res = subprocess.run("~/start.sh", shell=True, check=True)
    if DEBUG:
        print(f"Power ON: {res}")

def PowerOff():
    res = subprocess.run("~/stop.sh", shell=True, check=True)
    if DEBUG:
        print(f"Power OFF: {res}")

lastStatus = CheckSoundcardStatus()
while True:
    try:
        nowStatus = CheckSoundcardStatus()
    except Exception as ex:
        print(ex)
        time.sleep(1)
        continue

    if nowStatus:
        if not lastStatus:
            if DEBUG:
                print("Soundcard started")
            PowerOn()
            lastStatus = True
    else:
        if lastStatus:
            if DEBUG:
                print("Soundcard released")
            lastStatus = False
            lastIdle = Now()
        elif (not lastStatus) and lastIdle:
            if Now() - lastIdle >= SHUTDOWN_TIMEOUT:
                if DEBUG:
                    print("Timeout Reached")
                PowerOff()
                lastIdle = None
    time.sleep(0.5)

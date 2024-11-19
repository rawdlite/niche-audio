#!/usr/bin/env python3
from pysqueezebox import Server, Player
import tomllib
from pathlib import Path
import aiohttp
import asyncio
import argparse

parser = argparse.ArgumentParser(description='play next song')
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()

with open(Path.home() / ".config" / "niche-audio" / "config.toml", mode="rb") as fp:
    settings = tomllib.load(fp)

SERVER = settings['general']['server']
PLAYERNAME = settings['general']['player']
url = 'http://opml.radiotime.com/Tune.ashx?id=s25111&formats=aac,ogg,mp3&partnerId=16&serial=a44d9baf7190744ec4fa880f24a9fdba'
if args.verbose:
    print(f"server: {SERVER}\nplayer: {PLAYERNAME}")

async def main():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, SERVER)
        player = await lms.async_get_player(name=PLAYERNAME)
        await player.async_update()
        await player.async_load_url(url, cmd="load")
        await player.async_play()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

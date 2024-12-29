#!/usr/bin/env python3
from pysqueezebox import Server, Player
import tomllib
from pathlib import Path
import aiohttp
import asyncio
import argparse

with open(Path.home() / ".config" / "niche-audio" / "config.toml", mode="rb") as fp:
    settings = tomllib.load(fp)

SERVER = settings['general']['server']
PLAYERNAME = settings['general']['player']

parser = argparse.ArgumentParser(description='play next song')
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
parser.add_argument("-p", "--player", dest="player", default=PLAYERNAME)
args = parser.parse_args()

if args.verbose:
    print(f"server: {SERVER}\nplayer: {PLAYERNAME}")

async def main():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, SERVER)
        player = await lms.async_get_player(name=PLAYERNAME)
        await player.async_index("+1")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

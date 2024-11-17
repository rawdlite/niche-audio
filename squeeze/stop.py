#!/usr/bin/env python3
from pysqueezebox import Server, Player
import tomllib
from pathlib import Path
import aiohttp
import asyncio

with open(Path.home() / ".config" / "niche-audio" / "config.toml", mode="rb") as fp:
    settings = tomllib.load(fp)

DEBUG = settings['general']['debug']
SERVER = settings['general']['server']
#print(SERVER)
PLAYERNAME = settings['general']['player']

async def main():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, SERVER)
        player = await lms.async_get_player(name=PLAYERNAME)
        await player.async_update()
        await player.async_stop()
        print(player.mode)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

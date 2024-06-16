#!/usr/bin/env python3
from pysqueezebox import Server, Player
import aiohttp
import asyncio
SERVER = '192.168.178.4' # ip address of Logitech Media Server

async def main():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, SERVER)
        player = await lms.async_get_player(name="Moode")
        await player.async_update()
        await player.async_stop()
        print(player.mode)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

#!/usr/bin/python3
from pysqueezebox import Server, Player
import aiohttp
import asyncio
SERVER = '192.168.178.4' # ip address of Logitech Media Server
player_name = 'Moode'


async def main():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, SERVER)
        player = await lms.async_get_player(name=player_name)
        print("got player")
        await player.async_update()
        res = await player.async_query("playlist","shuffle","1")
        print(res)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

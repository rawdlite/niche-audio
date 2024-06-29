#!/usr/bin/python3
from pysqueezebox import Server, Player
import aiohttp
import asyncio
SERVER = 'dietpi5.fritz.box' # ip address of Logitech Media Server
player_name = 'Moode'

async def main():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, SERVER)
        player = await lms.async_get_player(name=player_name)
        await player.async_update()
        print(f"got player {player.player_id}")
        print(f"playing: {player.title}")
        #await player.async_play()
        print(f"remote: {player.remote}")
        #await player.async_update()
        print(f"current: {player.current_title}")
        print(f"track: {player.current_track}")
        print(f"remote: {player.remote_title}")
        print(f"type: {player.content_type}")
        res = await player.async_query("playlist","name","?")
        print(res)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

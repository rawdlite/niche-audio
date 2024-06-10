#!/usr/bin/python3
from pysqueezebox import Server, Player
import aiohttp
import asyncio
SERVER = '192.168.178.4' # ip address of Logitech Media Server
#url = 'qobuz://playlist/1208967'
url = 'http://open.qobuz.com/playlist/1208967'
#url = 'http://opml.radiotime.com/Tune.ashx?id=s25111&formats=aac,ogg,mp3&partnerId=16&serial=a44d9baf7190744ec4fa880f24a9fdba'
player_name = 'Moode'

async def main():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, SERVER)
        player = await lms.async_get_player(name=player_name)
        await player.async_update()
        await player.async_load_url(url, cmd="load")
        await player.async_play()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

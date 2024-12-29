#!/usr/bin/env python3
# cmd: "play" or "load" - replace current playlist (default)
# cmd: "play_now" - adds to current spot in playlist
# cmd: "insert" - adds next in playlist
# cmd: "add" - adds to end of playlist
from pysqueezebox import Server, Player
import os
import re
import tomllib
from pathlib import Path
import aiohttp
import asyncio
from argparse import ArgumentParser

with open(Path.home() / ".config" / "niche-audio" / "config.toml", mode="rb") as fp:
    settings = tomllib.load(fp)

SERVER = settings['general']['server'] # ip address of Logitech Media Server
PATH_ON_HOST = "/data/music/music_data"
PATH_IN_DOCKER = "/music"
PLAYER = settings['general']['player']

parser = ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
parser.add_argument("-c", "--cmd", dest="cmd", default="insert")
parser.add_argument("-s", "--server", dest="server", default=SERVER)
parser.add_argument("-p", "--player", dest="player", default=PLAYER)
parser.add_argument("-d", "--dir", dest="folder") 
parser.add_argument("files", nargs="*", type = str)
args = parser.parse_args()

if args.verbose: 
    print(f"file: {args.files}  cmd: {args.cmd}")
    print(f"player: {args.player} server: {args.server}")

async def main():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, args.server)
        player = await lms.async_get_player(name=args.player)
        if args.folder:
            files = [os.path.join(args.folder,f) for f in os.listdir(args.folder) if re.match('.*\.(mp3|flac)', f)]
        elif args.files:
            files = args.files
        #print(files)
        for file in files:
            url = f"file://{file.replace(PATH_ON_HOST,PATH_IN_DOCKER)}"
            await player.async_load_url(url, cmd=args.cmd)
        await player.async_update()
        if player.mode != 'play':
            await player.async_play()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

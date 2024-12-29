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

parser = argparse.ArgumentParser(description='show whats playing')
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
parser.add_argument("-s", "--server", dest="server", default=SERVER)
parser.add_argument("-p", "--player", dest="player", default=PLAYERNAME, required=False)
args = parser.parse_args()

if args.verbose:
    print(f"server: {args.server}\nplayer: >{args.player}<")

async def main():
    async with aiohttp.ClientSession() as session:
        lms = Server(session, args.server)
        if not lms:
            if args.verbose:
                print("could not get server")
            exit(1)
        player = await lms.async_get_player(name=args.player)
        if not player:
            if args.verbose:
                print("could not get player")
            exit(1)
        await player.async_update()
        if args.verbose:
            print(f"got player {player.player_id}")
        print(f"playing: {player.title}")
        print(f"remote: {player.remote}")
        print(f"current: {player.current_title}")
        print(f"track: {player.current_track}")
        print(f"remote: {player.remote_title}")
        print(f"type: {player.content_type}")
        res = await player.async_query("playlist","name","?")
        print(res)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

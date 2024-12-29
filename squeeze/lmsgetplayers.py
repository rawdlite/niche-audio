#!/usr/bin/env python3
from lms import Server, __version__
import argparse
import tomllib
from pathlib import Path

parser = argparse.ArgumentParser(description='play file')
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()

with open(Path.home() / ".config" / "niche-audio" / "config.toml", mode="rb") as fp:
    settings = tomllib.load(fp)

server = Server()
server.update()

for player in server.players:
    print(player.name)


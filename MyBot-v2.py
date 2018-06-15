import logging
import hlt
from collections import OrderedDict

game = hlt.Game("Milo")
logging.info("Starting Milo")

while True:
    game_map = game.update_map()
    command_queue = []

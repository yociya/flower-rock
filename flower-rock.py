import asyncio
import logging

from player import MusicPlayerBot
from speaker import TextSpeakerBot

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    TextSpeakerBot(loop)
    MusicPlayerBot(loop)
    # run loop
    loop.run_forever()

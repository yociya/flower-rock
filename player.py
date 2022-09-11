import discord
import os

import connector
import youtube

class MusicPlayerBot:

    def __init__(self, loop):
        MUSIC_TOKEN = os.environ['DISCORD_MUSIC_BOT_TOKEN']

        self.channelName = ''
        self.musicQue = youtube.AudioStatus()
        self.discord_client = discord.Client()
        self.discord_client.on_message = self.on_message
        self.discord_client.on_voice_state_update = self.on_voice_state_update

        loop.create_task(self.discord_client.start(MUSIC_TOKEN))

        print('ダンシングフラワーロックスタンバイ')

    async def frplay(self, message):
        if await connector.check_connect(message, 'レッツダンシング！', self.channelName, True):
            self.channelName = message.channel.name
        else:
            return
        
        keyword = message.content.replace('!frplay', '')
        if not self.musicQue.is_initialize():
            self.musicQue.start(message)

        await self.musicQue.add_audio(keyword)

    async def frskip(self, message):
        vc = message.guild.voice_client
        if vc.is_playing():
            vc.stop()

    async def frclean(self, message):
        await self.musicQue.clean()

    async def frlist(self, message):
        await self.musicQue.playlist(message)
    
    async def frpause(self, message):
        await self.musicQue.pause(message)

    async def frresume(self, message):
        await self.musicQue.resume(message)

    async def on_message(self, message):

        if message.author.bot:
            return

        if message.content.startswith('!frplay'):
            await self.frplay(message)
            return
        if message.content == '!frskip':
            await self.frskip(message)
            return
        if message.content == '!frclean':
            await self.frclean(message)
            return
        if message.content == '!frlist':
            await self.frlist(message)
            return
        if message.content == '!frpause':
            await self.frpause(message)
            return
        if message.content == '!frresume':
            await self.frresume(message)
            return
        
    async def on_voice_state_update(self, member, before, after):
        await connector.check_disconnect(member, before, after)

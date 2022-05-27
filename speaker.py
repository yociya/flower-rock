import discord
import os
import asyncio

from discord.embeds import Embed
from discord.player import FFmpegPCMAudio

import connector
import converter
import speech
import reminder

class TextSpeakerBot:

    def __init__(self, loop):
        TOKEN = os.environ['DISCORD_BOT_TOKEN']

        self.channelName = ''
        self.discord_client = discord.Client()
        self.discord_client.on_message = self.on_message
        self.discord_client.on_voice_state_update = self.on_voice_state_update
        self.reminder = reminder.Reminder()

        loop.create_task(self.discord_client.start(TOKEN))

        print('フラワーロックスタンバイ')

    async def frs(self, message):
        if await connector.check_connect(message, 'フラワーロックが咲きました', self.channelName, False):
            self.channelName = message.channel.name

    async def fre(self, message):
        vc = message.author.guild.voice_client
        if vc == None:
            print('まだ咲いてないよ！')
            await message.channel.send('まだ咲いてないよ！')
            return

        await message.channel.send('フラワーロックはしおれました')
        await vc.disconnect()
        await self.discord_client.close()

    async def help(self, message):
        text = ''
        linesplit = '\n'
        text += '!frs     咲くよ！' + linesplit
        text += '!fre     しおれるよ！' + linesplit
        text += '!frplay  音楽かけるよ！' + linesplit
        text += '!frskip  音楽とばすよ！' + linesplit
        text += '!frclean 待ってる音楽ふっとばすよ！' + linesplit
        text += '!frlist  待ってる音楽みるよ！' + linesplit
        text += '!frremind  リマインド作るよ！コマンド例/ !frremind ◯月◯日 ◯時 なんかやる' + linesplit
        text += '!frdelremind リマインド消すよ！イベントIDが必要だよ！' + linesplit
        text += '!frlistremind リマインドみるよ！' + linesplit
        
        embed = Embed(title='コマンドリスト', description=text)
        await message.channel.send(embed=embed)

    async def play_voice(self, message):
        vc = message.guild.voice_client

        text = converter.convert(message.content)
        if text == '':
            return
        ssml = speech.text_to_ssml(text)
        file = speech.ssml_to_speech(
            ssml, 
            str(message.channel.id) + '-' + str(message.author.id) + '-' + 'voice.mp3', 
            'ja-JP', 
        )

        while vc.is_playing():
            await asyncio.sleep(0.5)
        vc.play(FFmpegPCMAudio(file))


    async def on_message(self, message):

        if message.author.bot:
            return
        print(message.content)
        if message.content == '!frs':
            await self.frs(message)
            return
        if message.content == '!fre':
            await self.fre(message)
            return
        if message.content == '!frclose':
            raise KeyboardInterrupt
            return
        if message.content.startswith('!frremind'):
            await self.reminder.add_reminder(message)
            return
        if message.content.startswith('!frdelremind'):
            await self.reminder.del_reminder(message)
            return
        if message.content.startswith('!frlistremind'):
            await self.reminder.list_reminder(message)
            return
        if message.content == '!help' or message.content == '助けて！フラワーロック！':
            await self.help(message)
            return
        if message.content.startswith('!'):
            return
        if message.guild.voice_client == None:
            return
        if not message.guild.voice_client.is_connected():
            print('接続できてないみたい')
            return
        if self.channelName != message.channel.name:
            print('参加してないチャンネルのメッセージだよ！' + message.channel.name)
            return

        await self.play_voice(message)

    async def on_voice_state_update(self, member, before, after):
        await connector.check_disconnect(member, before, after)

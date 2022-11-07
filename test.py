import discord
import html
import os
import converter

from google.cloud import texttospeech
from discord.channel import VoiceChannel
from discord.player import FFmpegPCMAudio

TOKEN = os.environ['DISCORD_BOT_TOKEN']

client = discord.Client()

channelName = ''

async def connect_to_vc(message, isMove):
    global channelName

    vc = message.author.voice.channel
    if vc.name != message.channel.name:
        await message.channel.send('VCと対応してないチャンネルだよ！')
        return
    channelName = vc.name

    if isMove:
        vcc = message.author.guild.voice_client
        if vcc != None:
            await vcc.move_to(vc)
    else:
        await vc.connect()

    await message.channel.send('フラワーロックが咲きました')
    # print(vc.is_connected())

async def frs(message):
    global channelName

    if message.author.voice == None:
        await message.channel.send('VCに入ってないよ！')
        return
    
    if message.author.guild.voice_client != None:
        if message.author.voice.channel.name != channelName:
            await connect_to_vc(message, True)
            return
        await message.channel.send('すでにVCに入ってるよ！')
        return
    
    await connect_to_vc(message, False)

async def fre(message):
    global client

    vc = message.author.guild.voice_client
    if vc == None:
        print('まだ咲いてないよ！')
        await message.channel.send('まだ咲いてないよ！')
        return

    await message.channel.send('フラワーロックはしおれました')
    await vc.disconnect()
    await client.logout()

# @client.event
# async def on_disconnect():
#     global channelName

#     for vc in client.voice_clients:
#         await vc.disconnect()
#         for channel in client.guild.channles:
#             if channel.name == channelName:
#                 await channel.send('フラワーロックはしおれました')

def run_client():
    global client

    while True:
        @client.event
        async def on_ready():
            print('フラワーロックスタンバイ')

        @client.event
        async def on_message(message):
            global channelName

            if message.author.bot:
                return
            print(message.content)
            if message.content == '!frs':
                await frs(message)
                return
            if message.content == '!fre':
                await fre(message)
                return
            if message.content.startswith('!'):
                return
            if message.guild.voice_client == None:
                return
            print(message.guild.voice_client.is_connected())

            if channelName != message.channel.name:
                print('参加してないチャンネルのメッセージだよ！' + message.channel.name)
                return

            vc = message.guild.voice_client

        try:
            print('run')
            client.loop.run_until_complete(client.start(TOKEN))
        except KeyboardInterrupt:
            print('Keyboard Interrupt.')
            client.loop.close()
            print('program exit')
            return
        except Exception as e:
            print("Error", e)
        print('restart')
        client = discord.Client(loop=client.loop)

run_client()

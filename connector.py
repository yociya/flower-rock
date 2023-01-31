async def connect_to_vc(message, isMove):
    vc = message.author.voice.channel
    if vc.name != message.channel.name:
        await message.channel.send('VCと対応してないチャンネルだよ！')
        return False

    if isMove:
        vcc = message.author.guild.voice_client
        if vcc != None:
            await vcc.move_to(vc)
    else:
        await vc.connect()
        vcc = message.author.guild.voice_client
    
    return True

async def check_connect(message, on_success, current_channel, ignore_already):

    if message.author.voice == None:
        await message.channel.send('VCに入ってないよ！')
        return False
    
    if message.author.guild.voice_client != None:
        if message.author.voice.channel.name != current_channel:
            if await connect_to_vc(message, True):
                await message.channel.send(on_success)
            return True
        if not ignore_already:
           await message.channel.send('すでにVCに入ってるよ！')
        return True
    
    if await connect_to_vc(message, False):
        await message.channel.send(on_success)
        return True

async def check_disconnect(member, before, after):
    if member.bot:
        return
    if after.channel is None:
        vc = member.guild.voice_client
        if vc is None:
            return
        if vc.channel is before.channel:
            members = list(filter(lambda x: x.bot == False, vc.channel.members))
            print(members)
            if len(members) == 0:
                await vc.disconnect()

if __name__ == '__main__':
    print('connector')
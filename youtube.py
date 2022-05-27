import asyncio
import os
import time

from discord.player import FFmpegPCMAudio
from discord.embeds import Embed

from googleapiclient.discovery import build
import youtube_dl


TOKEN = os.environ['GOOGLE_API_TOKEN']

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

ffmpeg_options = {
    'options': '-vn'
}

class AudioQueue(asyncio.Queue):
    def __init__(self):
        super().__init__(0)
    def __getitem__(self, idx):
        return self._queue[idx]
    def to_list(self):
        return list(self._queue)
    def reset(self):
        self._queue.clear()

class AudioStatus:
    def __init__(self):
        self.vc = None
        self.channel = None
        self.queue = AudioQueue()
        self.playing = asyncio.Event()
        self.bgminfo = None
        self.playstart = 0
        self.pausetime = 0
        self.youtube_api = build('youtube', 'v3', developerKey=TOKEN)

    def start(self, message):
        self.vc = message.guild.voice_client
        self.channel = message.channel
        asyncio.create_task(self.playing_task())
    
    async def add_audio(self, keyWord):
        videoUrl = self.search(keyWord)
        if videoUrl == '':
            await self.channel.send('見つからなかったよ')
            return
        
        data = await play_url(videoUrl)
        
        if 'entries' in data:
            text = ''
            num = 0
            linesplit = '\n'
            for e in data['entries']:
                num += 1
                if num <= 10:
                    text += str(num) + '. ' + e['title'] + duration_to_min_sec(e['duration']) + linesplit
            if num > 10:
                text += '.....' + linesplit
            text += '計' + str(num) + '件'
            embed = Embed(title='追加したプレイリスト ' + data['title'], description=text)
            await self.channel.send(embed=embed)

            num = 0
            await self.queue.put(data['entries'][0])
            for e in data['entries']:
                num += 1
                if num == 1:
                    continue
                await self.queue.put(e)

        else:
            await self.channel.send(data['title'] + duration_to_min_sec(data['duration']) + ' をキューに追加したよ！')
            await self.queue.put(data)

    def play_next(self, err=None):
        duration = time.perf_counter() - self.playstart
        if not self.check_playtime(duration):
            self.retry(self.bgminfo, duration)
            return
        self.bgminfo = None
        self.playing.set()
        return
    
    def check_playtime(self, duration):
        if self.bgminfo['duration'] - duration > 30:
            return False
        return True

    def retry(self, data, duration):
        self.playstart = time.perf_counter()
        self.vc.play(FFmpegPCMAudio(data['url'] + '&t=' + str(duration) + 's', **ffmpeg_options), after = self.play_next)

    def is_initialize(self):
        return not (self.vc is None)
    
    def is_playing(self):
        return not (self.bgminfo is None)

    async def clean(self):
        self.queue.reset()
        return

    async def pause(self, message):
        if self.vc is None:
            return
        self.pausetime = time.perf_counter() - self.playstart
        self.vc.pause()
    
    async def resume(self, message):
        if self.vc is None:
            return
        self.playstart = time.perf_counter() - self.pausetime
        self.vc.resume()

    async def playlist(self, message):
        if self.vc is None:
            return
        text = ''
        num = 0
        linesplit = '\n'
        for e in self.queue.to_list():
            num += 1
            if num <= 10:
                text += str(num) + '. ' + e['title'] + duration_to_min_sec(e['duration']) + linesplit
        if num > 10:
            text += '.....' + linesplit
        text += '計' + str(num) + '件'
        embed = Embed(title='現在のキュー', description=text)
        await message.channel.send(embed=embed)
        return
    
    async def leave(self):
        self.queue.reset()
        if self.vc:
            self.vc = None
            self.channel = None
        return
    
    async def playing_task(self):
        while True:
            self.playing.clear()
            try:
                data = await asyncio.wait_for(self.queue.get(), timeout = 100)
            except asyncio.TimeoutError:
                print('TimeoutError')
                asyncio.create_task(self.leave())
                return
            # thumbnail
            text = data['title'] + ' を再生するよ'
            embed = Embed(title='次の曲', description=text)
            embed.add_field(name='URL', value=data['webpage_url'])
            embed.add_field(name='時間', value=duration_to_min_sec(data['duration']))
            embed.set_thumbnail(url=data['thumbnail'])
            await self.channel.send(embed=embed)
            # await self.channel.send(data['webpage_url'] + ' ' + duration_to_min_sec(data['duration']) + ' を再生するよ！')
            self.bgminfo = data
            self.playstart = time.perf_counter()
            self.vc.play(FFmpegPCMAudio(data['url'], **ffmpeg_options), after = self.play_next)
            await self.playing.wait()

    def search(self, keyword):
        print(keyword)
        if 'www.youtube.com' in keyword:
            return keyword.strip()

        response = self.youtube_api.search().list(
            q=keyword,
            part='id,snippet',
            maxResults=1
        ).execute()

        try:
            result = response['items'][0]['id']
            if result['kind'] == 'youtube#playlist':
                video_url = 'https://www.youtube.com/watch?list=' + str(result['playlistId'])
            else:
                video_url = 'https://www.youtube.com/watch?v=' + str(result['videoId'])
            
        except KeyError:
            print('KeyError')
            return ''
        print(video_url)
        return video_url

def duration_to_min_sec(duration):
    q, mod = divmod(duration, 60)
    if mod < 10:
        ssec = '0' + str(mod)
    else:
        ssec = str(mod)
    
    return '[' + str(q) + ':' + ssec + ']'

async def play_url(url):
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
    return data

if __name__ == '__main__':
    print('youtube')

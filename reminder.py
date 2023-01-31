import datetime
import os

from discord.embeds import Embed

from google.auth import load_credentials_from_file
from googleapiclient.discovery import build


class Reminder:
    def __init__(self):
        self.id = os.environ['CALENDAR_ID']

        # credentials = os.environ['GOOGLE_CREDENTIALS']
        # f = open('../google-credentials.json', 'w')
        # f.write(credentials)
        # f.close()

        self.channelName = ''
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = load_credentials_from_file(
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'], SCOPES)[0]
        self.calendar_api = build('calendar', 'v3', credentials=creds)

        print('モータルリマインダー')

    async def add_reminder(self, message):
        data = self.parse_message(message.content)
        cal_body = self.convert_insert_request(data)
        result = self.calendar_api.events().insert(calendarId=self.id,
                                                   body=cal_body).execute()
        await message.channel.send('スケジュール登録したよ イベントID：' + result["id"])

    async def del_reminder(self, message):
        eventId = message.content.replace('!frdelremind', '').trim()
        result = self.calendar_api.events().delete(calendarId=self.id,
                                                   eventId=eventId).execute()
        await message.channel.send('スケジュール削除したよ イベントID：' + eventId)

    async def list_reminder(self, message):
        text = ''
        events = self.search_request()
        linesplit = '\n'
        for event in events:
            text += self.format_time(
                event['start'].get('dateTime')
            ) + ' ' + event['summary'] + ' ' + event['id'] + linesplit

        embed = Embed(title='リマインドリスト', description=text)
        await message.channel.send(embed=embed)

    def format_time(self, time):
        return time.replace('-', '/').replace('+09:00', '').replace('T', ' ')

    def search_request(self):
        JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
        now = datetime.datetime.now(JST)
        result = self.calendar_api.events().list(
            calendarId=self.id,
            timeMin=now.isoformat(),
            maxResults=10,
            singleEvents=True,
            orderBy='startTime',
        ).execute()
        return result.get('items', [])

    def convert_insert_request(self, data):
        st = datetime.datetime(int(data['year']), int(data['month']),
                               int(data['day']), int(data['hour']),
                               int(data['minute']))
        body = {
            'summary': data['summary'],
            'description': data['summary'],
            'start': {
                'dateTime': st.isoformat(),
                'timeZone': 'Japan'
            },
            'end': {
                'dateTime': (st + datetime.timedelta(minutes=15)).isoformat(),
                'timeZone': 'Japan'
            }
        }
        print(body)
        return body

    def parse_message(self, message_txt):
        now = datetime.date.today()
        keywords = message_txt.replace('!frremind', '').split(' ')
        data = {}
        data['year'] = now.year
        data['month'] = now.month
        data['day'] = now.day
        data['hour'] = 12
        data['minute'] = 0
        for keyword in keywords:
            if self.parse_keyword(data, 'year', keyword, '年'):
                continue
            if self.parse_keyword(data, 'month', keyword, '月'):
                self.parse_year(data, keyword)
                continue
            if self.parse_keyword(data, 'day', keyword, '日'):
                self.parse_month(data, keyword)
                self.parse_year(data, keyword)
                continue
            if self.parse_keyword(data, 'hour', keyword, '時'):
                continue
            if self.parse_keyword(data, 'minute', keyword, '分'):
                self.parse_hour(data, keyword)
                continue
            data['summary'] = keyword

        return data

    def parse_year(self, data, keyword):
        if '年' in keyword:
            ss = keyword.split('年')
            data['year'] = ss[0]
            self.parse_month(data, ss[1])

    def parse_month(self, data, keyword):
        if '月' in keyword:
            ss = keyword.split('月')
            data['month'] = ss[0]
            self.parse_keyword(data, 'day', ss[1], '日')

    def parse_hour(self, data, keyword):
        if '時' in keyword:
            ss = keyword.split('時')
            data['hour'] = ss[0]
            self.parse_keyword(data, 'minute', ss[1], '分')

    def parse_keyword(self, data, data_key, keyword, search_txt):
        if keyword.endswith(search_txt):
            data[data_key] = keyword[:-1]
            return True
        return False


if __name__ == '__main__':
    clz = Reminder()
    data = clz.parse_message('!frremind 6月2日 14時 VLさんネット工事')
    print(data)
    data = clz.parse_message('!frremind 2023年6月2日 14時 VLさんネット工事')
    print(data)
    data = clz.parse_message('!frremind 2022年6月 14時 VLさんネット工事')
    print(data)
    data = clz.parse_message('!frremind 2022年6月 14時10分 VLさんネット工事')
    print(data)
    data = clz.parse_message('!frremind 2日 VLさんネット工事')
    print(data)
    dt = datetime.datetime(2022, 5, 27, 23, 48)
    print((dt + datetime.timedelta(minutes=15)).isoformat())

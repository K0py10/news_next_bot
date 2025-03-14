import sqlite3
from telethon import TelegramClient
from emoji import replace_emoji
from random import randint
from time import sleep
import json

channels_list = ["novosti_voinaa",
                 "rian_ru", 
                 "readovkanews", 
                 "bbbreaking", 
                 "ostorozhno_novosti", 
                 "voynareal", 
                 "wargonzo", 
                 "nexta_live", 
                 "meduzalive", 
                 "pravdadirty", 
                 "varlamov_news"]

with open("credentials.json" , 'r') as cr:
    data = json.load(cr)
    api_id = data["api_id"]
    api_hash = data["api_hash"]
parser = TelegramClient('anon', api_id, api_hash).start()
parser.parse_mode = None
# bot_token = "5909054565:AAHilbEQT8IozDDmn7b4i_GkN4XE2FxHTrQ"

con = sqlite3.connect("dataset.sql")
cur = con.cursor()

# cur.execute("DROP TABLE IF EXISTS posts")
# cur.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY AUTOINCREMENT, channel VARCHAR(16), text VARCHAR(4096))")
# res = cur.execute("SELECT * FROM posts")
# for row in res.fetchall():
#     print(str(row))


async def get_channel_messages(channel, amount, start_id):
    res = []
    if start_id < 0:
        print("-1")
        async for msg in parser.iter_messages(channel, limit = 1): #getting last message from channel
            print("start_id acqired")
            start_id = msg.id
    async for msg in parser.iter_messages(channel, limit = amount, max_id = start_id, wait_time=1): # max_id = start_id
        try: 
            # print("Message received from" + channel)
            print(msg.text)
            if len(msg.raw_text) > 64: 
                res.append(({"channel": channel, "text": replace_emoji(msg.raw_text.replace("\n", " "), replace = '')}))
        except Exception as e:
            print("An error occurred: " + str(e))
    if len(res) < amount:
        add = await get_channel_messages(channel, amount - len(res), start_id = start_id - amount)
        print("sent again")
        res += add
    return res

for ch in channels_list:
    print(ch)
    posts = parser.loop.run_until_complete(get_channel_messages(ch, 1, -1))
    # cur.executemany("INSERT INTO posts (channel, text) VALUES (:channel, :text)", posts)
    con.commit()
    # for row in cur.execute("SELECT * FROM posts").fetchall():
    #     print(row)
    sleep(randint(1, 10))

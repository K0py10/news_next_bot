from telethon.sync import TelegramClient
from telethon.sync import events

api_id = 23941955
api_hash = "cdb1e1510a9e8a5c9c6ff0851c829c33"

# make sure you have defined api_id, api_has, bot_token somewhere in the code
bot = TelegramClient('bot', api_id,  api_hash).start(bot_token="5861496186:AAFOFoLjBf-UoS9it_dpx0r1C2qzjiFmEh0")
@bot.on(events.NewMessage)
async def any_message_arrived_handler(event):
    print('We are handling message events')

bot.run_until_disconnected()
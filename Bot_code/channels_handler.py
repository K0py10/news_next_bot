from telethon import *

api_id = 23941955
api_hash = "cdb1e1510a9e8a5c9c6ff0851c829c33"

bot = TelegramClient('bot', api_id,  api_hash).start(bot_token="5861496186:AAFOFoLjBf-UoS9it_dpx0r1C2qzjiFmEh0")

channels_list = [] #TEMPORARY
offset_id = 0
limit = 100
all_messages = []
total_messages = 0
total_count_limit = 0

greeting_text = "Shalom, my friend"
help_text = "**Commands List**: \n /add_channel - Add channel to list of channels, whose posts will be fetched (Thereafter – list of channels)"

addChannel_mode = False

@bot.on(events.NewMessage(pattern = "/start"))
async def any_message_arrived_handler(event):
    if event.user_id not in channels_list:
        channels_list.append([event.id, 0])
    await event.reply(greeting_text)

@bot.on(events.NewMessage(pattern = "/help"))
async def any_message_arrived_handler(event):
    await event.reply(help_text)

@bot.on(events.NewMessage(pattern = "/add_channel.+"))
async def any_message_arrived_handler(event):
    if add_channel(event): 
            await event.reply("Channel added")
    else:
            await event.reply("Somethong went wrong, try again")
    #await event.reply("Send me a link to the channel with or without t.me/ part")


def add_channel(user_message_event):
    try:
        channels_list[channels_list.find(user_message_event.user_id)].append(bot.get_entity(user_message_event.text))
        print(channels_list)
        return True
    except Exception as e:
        print(channels_list)
        return False
    
while True:
    print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
    history = bot.Get(peer = channels_list[0], offset_id=offset_id, offset_date=None, add_offset=0, limit=limit, max_id=0, min_id=0, hash=0)
    if not history.messages:
        break
    messages = history.messages
    for message in messages:
        all_messages.append(message.to_dict())
    offset_id = messages[len(messages) - 1].id
    total_messages = len(all_messages)
    if total_count_limit != 0 and total_messages >= total_count_limit:
        break


bot.start()
bot.run_until_disconnected()
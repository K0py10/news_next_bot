from telethon.sync import TelegramClient, events, PeerChannel, GetHistoryRequest

api_id = 23941955
api_hash = "cdb1e1510a9e8a5c9c6ff0851c829c33"
bot = TelegramClient('bot', api_id,  api_hash).start(bot_token="5861496186:AAFOFoLjBf-UoS9it_dpx0r1C2qzjiFmEh0")

channels_list = [] #TEMPORARY
offset_id = 0
limit = 100
all_messages = []
total_messages = 0
total_count_limit = 0

while True:
    print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
    history = bot.GetHistoryRequest(peer = channels_list[0], offset_id=offset_id, offset_date=None, add_offset=0, limit=limit, max_id=0, min_id=0, hash=0)
    if not history.messages:
        break
    messages = history.messages
    for message in messages:
        all_messages.append(message.to_dict())
    offset_id = messages[len(messages) - 1].id
    total_messages = len(all_messages)
    if total_count_limit != 0 and total_messages >= total_count_limit:
        break
        


def add_channel(channel_user_input):
    if channel_user_input.isdigit():
        entity = PeerChannel(int(channel_user_input))
    else:
        entity = channel_user_input

    channels_list.append(bot.get_entity(entity))


# make sure you have defined api_id, api_has, bot_token somewhere in the code
@bot.on(events.NewMessage)
async def any_message_arrived_handler(event):
    print('We are handling message events')


bot.run_until_disconnected()
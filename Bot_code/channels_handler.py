from telethon import TelegramClient
#from asyncio import *
#from telethon.sync import TelegramClient 
#from telethon.tl.functions.messages import GetHistory 

api_id = 23941955
api_hash = "cdb1e1510a9e8a5c9c6ff0851c829c33"
 #bot_token="5861496186:AAFOFoLjBf-UoS9it_dpx0r1C2qzjiFmEh0"
bot = TelegramClient('anon', api_id, api_hash).start()

channel_entity = "" #TEMPORARY SOLUTION
channel_lastmessage = ""

'''
async def add_channel_id(user_message_text):
    try:
        loop = new_event_loop()
        set_event_loop(loop)
        channel_entity = await bot.get_entity(user_message_text)
        print("Channel: ", channel_entity)
        return channel_entity
    except Exception as e:
        print(e, "Channel: ", channel_entity)
        #print(e, "Last messages: ", channels_lastmessages_list)
        return -1
'''

async def add_message_to_channels_list(channel_username):
    channel_lastmessage = -1
    try: 
        print("Started fetching messages from channel")
        async for msg in bot.iter_messages(channel_username, limit = 1):
            print("Msg:", msg.text)
            channel_lastmessage = msg.id
        return channel_lastmessage 
    except Exception as e:
        print(e, "Channel last message's id: ", channel_lastmessage)
        return -1

async def retrieve_messages(user_entity, channels_list): #, last_message_id
    for i in range(len(channels_list)):
        messages_to_forward = bot.iter_messages(channels_list[i], reverse = True)
        for msg in messages_to_forward:
            #messages_to_forward = bot.iter_messages(channel_entity, min_id = last_message_id)
            print(msg)
            await bot.forward_messages(user_entity, msg)
'''    
while True:
    print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
    history = bot.GetHistory(peer = channels_list[0], offset_id=offset_id, offset_date=None, add_offset=0, limit=limit, max_id=0, min_id=0, hash=0)
    if not history.messages:
        break 
    messages = history.messages
    for message in messages:
        all_messages.append(message.to_dict())
    offset_id = messages[len(messages) - 1].id
    total_messages = len(all_messages)
    if total_count_limit != 0 and total_messages >= total_count_limit:
        break
'''

bot.run_until_disconnected()
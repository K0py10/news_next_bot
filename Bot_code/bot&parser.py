from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telethon import TelegramClient
#from channels_handler import add_message_to_channels_list

api_id = 23941955
api_hash = "cdb1e1510a9e8a5c9c6ff0851c829c33"
bot_token="5861496186:AAFOFoLjBf-UoS9it_dpx0r1C2qzjiFmEh0"
parser = TelegramClient('anon', api_id, api_hash).start()

channels_list = ['@shitpost_of_myself'] #TEMPORARY AS HELL SOLUTION
channels_lastmessages_list = [10]

greeting_text = "Hello. \nI'm a bot, designed to unite all channels' posts in one place.\nTo get commands list, type /help"
help_text = "Commands List: \n /add_channel - Add channel to list of channels, whose posts will be fetched (Thereafter – list of channels)"
channel_added_text = "Channel added successfully"
channel_adding_error_text = "Something went wrong, check your input and try again"
'''
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INF
)
'''

async def start_CR(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(update.effective_chat.id, greeting_text) #send_message(chat_id=update..id, text="I'm a bot, please talk to me!")

async def help_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /help command
	await context.bot.send_message(update.effective_chat.id, help_text) 

async def add_channel_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /add_channel command
    if await register_channel(update.message.text.replace("/add_channel ", "")):
        print ("Channels: ", channels_list) 
        print ("Last messages: ", channels_lastmessages_list)
        await context.bot.send_message(update.effective_chat.id, channel_added_text) 
    else:
        await context.bot.send_message(update.effective_chat.id, channel_adding_error_text) 

async def retrieve_messages_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #, last_message_id
    for i in range(len(channels_list)):
        async for msg in parser.iter_messages(channels_list[i], reverse = True):
            print ("Message: ", msg.text)
            #try: 
                #path = await msg.download_media()
            #finally:
            await context.bot.send_message(update.effective_chat.id, text = msg.text)
            #print("nudes acquired")



async def register_channel(channel_user_input): 
    try:
        channel_entity = await parser.get_entity(channel_user_input)
        channels_list.append(channel_entity.username)
        print ("Channel name: ", channel_entity.username)
        channel_lastmessage = -1
        channel_lastmessage = await add_message_to_channels_list(channel_user_input)

        if channel_lastmessage != -1:
            channels_lastmessages_list.append(channel_lastmessage)
            return True
        else:
            return False
    except: return False

async def add_message_to_channels_list(channel_username): #TELETHON FUNCTION
    channel_lastmessage = -1
    print("Started fetching messages from channel")

    async for message in parser.iter_messages(channel_username, limit = 1):
        #print(message.id, message.text)
        channel_lastmessage = message.id
    return channel_lastmessage



if __name__ == "__main__":
    application = ApplicationBuilder().token(bot_token).build()
    application.add_handler(CommandHandler('start', start_CR))
    application.add_handler(CommandHandler('help', help_CR))
    application.add_handler(CommandHandler('add_channel', add_channel_CR))   
    application.add_handler(CommandHandler('retrieve_messages', retrieve_messages_CR)) 

    application.run_polling()

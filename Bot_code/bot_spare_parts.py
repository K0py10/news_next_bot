'''from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext.dispatcher import run_async
from telethon.sync import TelegramClient
#from channels_handler import add_message_to_channels_list #add_channel_id

api_id = 23941955
api_hash = "cdb1e1510a9e8a5c9c6ff0851c829c33"
bot_token="5861496186:AAFOFoLjBf-UoS9it_dpx0r1C2qzjiFmEh0"
#bot = TelegramClient('anon', api_id, api_hash)
updater = Updater(bot_token, use_context=True)



greeting_text = "Hello. \nI'm a bot, designed to unite all channels' posts in one place.\nTo get commands list, type /help"
help_text = "Commands List: \n /add_channel - Add channel to list of channels, whose posts will be fetched (Thereafter – list of channels)"

def start(update: Update, context: CallbackContext): #response to /start command
	update.message.reply_text(greeting_text)

def help(update: Update, context: CallbackContext): #response to /help command
	update.message.reply_text(help_text)

@run_async
async def add_channel(update: Update, context: CallbackContext): #response to /add_channel command
    if await register_channel(update.message.text.replace("/add_channel ", "")):
        print ("Channels: ", channels_list) 
        print ("Last messages: ", channels_lastmessages_list)
        update.message.reply_text("Channel added successfully")
    else:
        update.message.reply_text("Something went wrong, check your input and try again")
    #update.message.reply_text("Send me a link to the channel with or without t.me/ part")

def unknown(update: Update, context: CallbackContext):  
    update.message.reply_text("I'm sorry, '%s' is a not a valid command" % update.message.text) 


async def register_channel(channel_user_input): 
    channels_list.append(channel_user_input)
    print("Channels: ", channels_list)
    #loop = set_event_loop(new_event_loop())
    channel_lastmessage = -1
    with bot:
        channel_lastmessage = add_message_to_channels_list(channel_user_input)

    if channel_lastmessage != -1:
        channels_lastmessages_list.append(channel_lastmessage)
        print("Last messages: ", channels_lastmessages_list)
        return True
    else:
        channels_list.pop(-1)
        return False


def add_message_to_channels_list(channel_username): #TELETHON FUNCTION
    channel_lastmessage = -1
    print("Started fetching messages from channel")

    for message in bot.iter_messages('https://t.me/shitpost_of_myself', limit = 1):
        print(message.id, message.text)
        channel_lastmessage = message.id
    return channel_lastmessage
        # You can download media from messages, too!
        # The method will return the path where the file was saved.
        #if message.photo:
            #path = await message.download_media()
            #print('File saved to', path)  # printed after download is done



updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('add_channel', add_channel))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.run_async(add_channel)
#updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
updater.start_polling()
'''
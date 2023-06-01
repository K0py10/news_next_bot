from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from telethon import TelegramClient 
from multiprocessing import Process
from os import remove
from cleaner import clean_text
from entities_parser import parse_entities
import db_handler
import json
import asyncio
from random import randint
import sqlite3

#from channels_handler import add_message_to_channels_list

with open("credentials.json" , 'r') as cr:
    data = json.load(cr)
    api_id = data["api_id"]
    api_hash = data["api_hash"]
    bot_token = data["bot_token"]
parser = TelegramClient('anon', api_id, api_hash).start()
parser.parse_model = 'html'
application = ApplicationBuilder().token(bot_token).build()
bot = application.bot
con = sqlite3.connect('db.sql')
cur = con.cursor()

db_handler.restart_db(cur)

greeting_text = "Hello. \nI'm a bot, designed to unite all channels' posts in one place.\nTo get commands list, type /help"
help_text = "Commands List: \n /add_channel - Add channel to list of channels, whose posts will be fetched (Thereafter – list of channels)"
channel_added_text = "Channel added successfully"
channel_adding_error_text = "Something went wrong, check your input and try again"

def run_parser():
    while True:
        print('fuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuck')
        parser.loop.run_until_complete(update())
        asyncio.sleep(1)

async def start_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /start command
    await context.bot.send_message(update.effective_chat.id, greeting_text) 
async def help_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /help command
	await context.bot.send_message(update.effective_chat.id, help_text)       
async def add_channel_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #response to /add_channel command
    if await add_channel(update.message.text.replace("/add_channel ", ""), update.effective_chat.id):
        await context.bot.send_message(update.effective_chat.id, channel_added_text) 
    else:
        await context.bot.send_message(update.effective_chat.id, channel_adding_error_text) 
async def retrieve_messages_CR(update: Update, context: ContextTypes.DEFAULT_TYPE): #, last_message_id
    channels_list = db_handler.get_all_channels(cur)
    print("channels list: " + str(channels_list))
    for ch in channels_list:
        last_id = 0
        print('channel' + str(ch))
        async for msg in parser.iter_messages(ch[1], min_id = ch[2], reverse = True): #iterate over new channel messages
            last_id = msg.id
            try:
                if msg.raw_text != None: #sort out technical messages
                    entity = await parser.get_entity(ch[1])
                    text_to_send = entity.title + ":\n" +  msg.text + "\nhttps://t.me/" + entity.username + "/" + str(msg.id)
                    await context.bot.send_message(update.effective_chat.id, text = text_to_send, parse_mode='HTML')
            except Exception as e:
                print("Parsing message failed\nException: ", e, "\nText:", msg.text, "\nID", msg.id)
        if last_id != 0:    
            db_handler.update_last_message(cur, ch[0], last_id)

async def add_channel(channel_user_input, chat_id): #
    try:
        entity = await parser.get_entity(channel_user_input)
        name = entity.username  
        #getting telegram's internal channel entity (used to verify thet the link is valid and unify stored data)
        channel_lastmessage = -1 #used for handling errors
        channel_lastmessage = await get_channel_lm(name)
        if channel_lastmessage != -1:
            db_handler.save_channel(cur, name, channel_lastmessage - randint(1, 10), chat_id)
            return True
        else:
            return False
    except Exception as e: 
        print("error: " + str(e))
        return False
async def get_channel_lm(channel_username):
    channel_lastmessage = -1
    async for message in parser.iter_messages(channel_username, limit = 1): #getting last message from channel
        channel_lastmessage = message.id #saving its id
    return channel_lastmessage

async def update():
    channels_list = db_handler.get_all_channels()
    for ch in channels_list:
        if get_channel_lm(ch[1]) != ch[2]: #if there are new messages
            dest_list = db_handler.get_channel_subs(cur, ch[0])
            last_id = 0
            async for msg in parser.iter_messages(ch[1], min_id = ch[2], reverse=True):
                try:
                    last_id = msg.id
                    if msg.text != None:
                        entity = await parser.get_entity(ch[1])
                        text_to_send = entity.title + ":\n" +  msg.text + "\nhttps://t.me/" + entity.username + "/" + str(msg.id)
                        for sub in dest_list:
                            try:
                                await bot.send_message(sub, text = text_to_send, parse_mode='HTML')
                            except Exception as e:
                                print("Parsing message failed\nException: ", e, "\nChat_id:", sub, "\nChannel: ", ch[1], "\nID: ", msg.id)
                except Exception as e:
                    print("Parsing message failed\nException: ", e, "\nChat_id:", sub, "\nChannel: ", ch[1], "\nID: ", msg.id)
            if last_id != 0:
                db_handler.update_last_message(cur, ch[0], last_id)

if __name__ == "__main__":
    application.add_handler(CommandHandler('start', start_CR))
    application.add_handler(CommandHandler('help', help_CR))
    application.add_handler(CommandHandler('add_channel', add_channel_CR))   
    application.add_handler(CommandHandler('retrieve_messages', retrieve_messages_CR)) 

    Process(target=run_parser).start()
    Process(target=application.run_polling()).start()


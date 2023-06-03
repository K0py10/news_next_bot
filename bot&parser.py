from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Updater, MessageHandler, filters
from telethon import TelegramClient 
from multiprocessing import Process
from os import remove
from unused.cleaner import clean_text
from unused.entities_parser import parse_entities
import db_handler as db
import json
import asyncio
from random import randint
import simularity_handler as sh
import time
import sqlite3
from emoji import replace_emoji

#from channels_handler import add_message_to_channels_list

with open("credentials.json" , 'r') as cr:
    data = json.load(cr)
    api_id = data["api_id"]
    api_hash = data["api_hash"]
    bot_token = data["bot_token"]
parser = TelegramClient('anon', api_id, api_hash).start()
parser.parse_mode = 'html'
application = ApplicationBuilder().token(bot_token).build()
bot = application.bot
con = sqlite3.connect('db.sql')
cur = con.cursor()

db.restart_db(cur)

greeting_text = "Hello. \nI'm a bot, designed to unite all channels' posts in one place.\nTo get commands list, type /help"
help_text = "Commands List: \n /add_channel - Add channel to list of channels, whose posts will be fetched (Thereafter – list of channels)"
channel_added_text = "Channel added successfully"
channel_adding_error_text = "Something went wrong, check your input and try again"

async def run():
    await application.initialize()
    await application.updater.start_polling()
    await application.start()
    while True:
        try:
            await bot.get_updates()
            await update()
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit) as e:
            break
        except Exception as e:
            print("ERROR:", + str(e))

    application.updater.stop()
    application.stop()
    application.shutdown()

def run_updater(parser):
    while True:
        try:
            asyncio.run(update(parser))
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit) as e:
            break

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
    channels_list = db.get_all_channels(cur)
    print("channels list: " + str(channels_list))
    for ch in channels_list:
        last_id = 0
        print('channel' + str(ch))
        async for msg in parser.iter_messages(ch.name, min_id = ch.last_message, reverse = True): #iterate over new channel messages
            last_id = msg.id
            try:
                cleaned_text = replace_emoji(msg.raw_text.replace("\n", " "), replace = '')
                post_id = db.save_post(cur, ch.id, cleaned_text, sh.prepare_text(cleaned_text))

                db.add_post_to_chat(cur, Update.effective_chat_id, post_id)

                if msg.raw_text != None and msg.raw_text != '': #sort out technical messages
                    entity = await parser.get_entity(ch[1])
                    text_to_send = entity.title + ":\n" +  msg.text + "\nhttps://t.me/" + entity.username + "/" + str(msg.id)
                    await context.bot.send_message(update.effective_chat.id, text = text_to_send, entities= [MessageEntity('BOLD', 1, len(entity.title) + 1)], parse_mode='HTML', disable_web_page_preview=True)
            except Exception as e:
                print("Parsing message failed\nException: ", e, "\nText:", msg.text, "\nID", msg.id)
        if last_id != 0:    
            db.update_last_message(cur, ch[0], last_id)

async def add_channel(channel_user_input, chat_id): #
    try:
        entity = await parser.get_entity(channel_user_input)
        name = entity.username  
        #getting telegram's internal channel entity (used to verify thet the link is valid and unify stored data)
        channel_lastmessage = -1 #used for handling errors
        channel_lastmessage = await get_channel_lm(name)
        if channel_lastmessage != -1:
            db.save_channel(cur, name, channel_lastmessage - randint(1, 10), chat_id)
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

async def update(parser):
    print('calling telethon update')
    channels_list = db.get_all_channels(cur)
    for ch in channels_list:
        if get_channel_lm(ch[1]) != ch[2]: #if there are new messages
            dest_list = db.get_channel_subs(cur, ch[0])
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
                db.update_last_message(cur, ch[0], last_id)

if __name__ == "__main__":
    application.add_handler(CommandHandler('start', start_CR))
    application.add_handler(CommandHandler('help', help_CR))
    application.add_handler(CommandHandler('add_channel', add_channel_CR))   
    application.add_handler(CommandHandler('retrieve_messages', retrieve_messages_CR)) 

    application.run_polling()
    asyncio.run(run())

    # parser_process = Process(target = run_updater, args=(parser,))
    # parser_process.start()
    # parser_process.join()

    # bot_process = Process(target = application.run_polling())
    # parser_process.start()
    # parser_process.join()

    # print("about to start bot")
    # bot_loop = asyncio.new_event_loop()
    # bot_loop.run_until_complete(application.initialize())
    # bot_loop.run_until_complete(application.updater.start_polling())
    # bot_loop.run_until_complete(application.start())

    # while True:
    #     try:
    #         parser.loop.run_until_complete(update())
    #         time.sleep(1)
    #     except (KeyboardInterrupt, SystemExit) as e:
    #         break
    #     except Exception as e:
    #         print("ERROR:", + str(e))

    # bot_loop.run_until_complete(application.updater.stop())
    # bot_loop.run_until_complete(application.stop())
    # bot_loop.run_until_complete(application.shutdown())